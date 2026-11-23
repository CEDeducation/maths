"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  ClipboardCheck,
  LockKeyhole,
  RotateCcw,
  Trophy,
  XCircle,
} from "lucide-react";

import { Breadcrumbs, ProgressBar } from "@/components/UI";
import {
  chapterById,
  lessonsForChapter,
  questionsForTest,
  trackById,
} from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";

export default function TestPage() {
  const { chapterId } = useParams<{ chapterId: string }>();

  const chapter = chapterById(chapterId);
  const questions = questionsForTest(chapterId);
  const track = chapter
    ? trackById(chapter.trackId)
    : undefined;

  const { saveTest } = useProgress();

  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>(
    Array(10).fill(-1)
  );
  const [finished, setFinished] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setIndex(0);
    setAnswers(Array(10).fill(-1));
    setFinished(false);
    setSaving(false);
    setMessage("");
  }, [chapterId]);

  const answered = answers.filter(
    (answer) => answer !== -1
  ).length;

  const score = questions.filter(
    (question, i) =>
      answers[i] === question.answerIndex
  ).length;

  async function submit() {
    if (
      !chapter ||
      saving ||
      answered !== questions.length ||
      questions.length !== 10
    ) {
      return;
    }

    const currentChapterId = chapter.id;
    setSaving(true);

    try {
      const result = await saveTest(
        currentChapterId,
        score,
        questions.length,
        answers
      );

      setMessage(
        result.message ||
          (result.ok
            ? "Assessment saved successfully."
            : "Assessment could not be saved.")
      );
    } catch {
      setMessage(
        "Could not save your score. Please try again later."
      );
    } finally {
      setFinished(true);
      setSaving(false);
    }
  }

  function retry() {
    setIndex(0);
    setAnswers(Array(10).fill(-1));
    setFinished(false);
    setSaving(false);
    setMessage("");
  }

  function chooseAnswer(optionIndex: number) {
    setAnswers((previous) =>
      previous.map((answer, questionIndex) =>
        questionIndex === index ? optionIndex : answer
      )
    );
  }

  if (!chapter || !track || questions.length !== 10) {
    return (
      <div className="blank-state">
        Chapter checkpoint unavailable.{" "}
        <Link href="/">Return home</Link>
      </div>
    );
  }

  const question = questions[index];
  const percent = Math.round(
    (score / questions.length) * 100
  );

  return (
    <div className="page-enter">
      <Breadcrumbs
        parts={[
          {
            title: track.title,
            href: `/track/${track.id}`,
          },
          {
            title: chapter.title,
            href: `/track/${track.id}`,
          },
          {
            title: "Chapter checkpoint",
          },
        ]}
      />

      {finished ? (
        <div className="test-results">
          <div className="results-card test-results-summary">
            <span className="results-trophy">
              <Trophy size={41} />
            </span>

            <span className="section-kicker">
              CHAPTER CHECKPOINT COMPLETE
            </span>

            <h1>
              {score >= 7
                ? "Checkpoint passed!"
                : "Keep learning. You've got this."}
            </h1>

            <p>
              {chapter.title} · {questions.length} questions
            </p>

            <div className="score-display">
              <strong>
                {score}
                <span> / {questions.length}</span>
              </strong>

              <span>{percent}% correct</span>
            </div>

            <ProgressBar
              percent={percent}
              color={score >= 7 ? "mint" : "coral"}
              height={12}
            />

            {message && (
              <p className="save-message">{message}</p>
            )}

            <div className="result-actions">
              <button
                type="button"
                className="button button-outline"
                onClick={retry}
              >
                <RotateCcw size={16} />
                Retake test
              </button>

              <Link
                className="button button-primary"
                href={`/track/${track.id}`}
              >
                Back to {track.title}
                <ArrowRight size={16} />
              </Link>
            </div>
          </div>

          <div className="review-list">
            <h2>Review your answers</h2>

            <p>
              Check each solution to understand
              what worked and what to revise.
            </p>

            {questions.map((item, questionIndex) => {
              const isCorrect =
                answers[questionIndex] === item.answerIndex;

              return (
                <article
                  className="review-item"
                  key={item.id}
                >
                  <span
                    className={`review-marker ${
                      isCorrect ? "positive" : "negative"
                    }`}
                  >
                    {isCorrect ? (
                      <CheckCircle2 size={21} />
                    ) : (
                      <XCircle size={21} />
                    )}
                  </span>

                  <div>
                    <span className="small-overline">
                      QUESTION {questionIndex + 1} ·{" "}
                      {item.skill}
                    </span>

                    <h3>{item.prompt}</h3>

                    <p>
                      Your answer:{" "}
                      <b>
                        {item.options[
                          answers[questionIndex]
                        ] ?? "Unanswered"}
                      </b>
                    </p>

                    <p>
                      Correct answer:{" "}
                      <b className="green-text">
                        {item.options[item.answerIndex]}
                      </b>
                    </p>

                    <div className="review-solution">
                      <strong>Why?</strong>{" "}
                      {item.explanation.join(" ")}
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="test-layout">
          <div className="test-heading">
            <span className="section-kicker">
              CHAPTER {chapter.order} ASSESSMENT
            </span>

            <h1>
              {chapter.title}: Checkpoint
            </h1>

            <p>
              10 questions across{" "}
              {lessonsForChapter(chapter.id).length}{" "}
              subtopics. No hints until you
              finish—just like a classroom quiz.
            </p>

            <div className="test-note">
              <LockKeyhole size={16} />
              Your score and explanations appear
              only after submission.
            </div>
          </div>

          <div className="test-two-col">
            <div className="question-card test-question">
              <div className="question-topline">
                <span className="question-tag">
                  <ClipboardCheck size={16} />
                  CHAPTER TEST
                </span>

                <span className="question-number">
                  {index + 1} / {questions.length}
                </span>
              </div>

              <h2 className="question-prompt">
                {question.prompt}
              </h2>

              <div
                className="answer-options"
                role="radiogroup"
                aria-label="Answer choices"
              >
                {question.options.map(
                  (option, optionIndex) => (
                    <button
                      key={`${index}-${optionIndex}`}
                      type="button"
                      role="radio"
                      aria-checked={
                        answers[index] === optionIndex
                      }
                      className={`answer-option ${
                        answers[index] === optionIndex
                          ? "selected"
                          : ""
                      }`}
                      onClick={() =>
                        chooseAnswer(optionIndex)
                      }
                    >
                      <span className="option-letter">
                        {String.fromCharCode(
                          65 + optionIndex
                        )}
                      </span>

                      {option}
                    </button>
                  )
                )}
              </div>

              <div className="question-footer">
                <button
                  type="button"
                  className="button button-ghost"
                  disabled={index === 0}
                  onClick={() =>
                    setIndex((i) => i - 1)
                  }
                >
                  <ArrowLeft size={16} />
                  Previous
                </button>

                {index < questions.length - 1 ? (
                  <button
                    type="button"
                    className="button button-primary"
                    onClick={() =>
                      setIndex((i) => i + 1)
                    }
                  >
                    Next question
                    <ArrowRight size={16} />
                  </button>
                ) : (
                  <button
                    type="button"
                    className="button button-primary"
                    disabled={
                      answered !== questions.length ||
                      saving
                    }
                    onClick={submit}
                  >
                    {saving
                      ? "Saving..."
                      : "Submit checkpoint"}

                    <CheckCircle2 size={17} />
                  </button>
                )}
              </div>
            </div>

            <aside className="test-navigator">
              <span className="small-overline">
                YOUR PROGRESS
              </span>

              <h3>
                {answered} of {questions.length} answered
              </h3>

              <ProgressBar
                percent={
                  (answered / questions.length) * 100
                }
                height={9}
              />

              <div className="test-number-grid">
                {questions.map(
                  (item, questionIndex) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() =>
                        setIndex(questionIndex)
                      }
                      className={`${
                        index === questionIndex
                          ? "current"
                          : ""
                      } ${
                        answers[questionIndex] !== -1
                          ? "answered"
                          : ""
                      }`}
                      aria-label={`Go to question ${
                        questionIndex + 1
                      }`}
                    >
                      {questionIndex + 1}
                    </button>
                  )
                )}
              </div>

              <p>
                You can jump between questions
                and change answers before submitting.
              </p>

              <button
                type="button"
                className="button button-primary full-width"
                disabled={
                  answered !== questions.length ||
                  saving
                }
                onClick={submit}
              >
                {saving
                  ? "Saving..."
                  : answered === questions.length
                  ? "Submit test"
                  : "Answer all 10 questions"}

                <ArrowRight size={16} />
              </button>

              <Link
                href={`/track/${track.id}`}
                className="test-back"
              >
                Leave checkpoint
              </Link>
            </aside>
          </div>
        </div>
      )}
    </div>
  );
}
