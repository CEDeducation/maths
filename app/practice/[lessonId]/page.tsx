"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Lightbulb,
  RotateCcw,
  Sparkles,
  Target,
  Trophy,
  XCircle,
} from "lucide-react";

import { Breadcrumbs, ProgressBar } from "@/components/UI";
import {
  chapterById,
  lessonById,
  questionsForLesson,
  trackById,
} from "@/lib/curriculum";
import { useProgress } from "@/lib/progress";

export default function PracticePage() {
  const { lessonId } = useParams<{ lessonId: string }>();

  const lesson = lessonById(lessonId);
  const items = questionsForLesson(lessonId);

  const chapter = lesson
    ? chapterById(lesson.chapterId)
    : undefined;

  const track = chapter
    ? trackById(chapter.trackId)
    : undefined;

  const { savePractice } = useProgress();

  const [index, setIndex] = useState(0);
  const [chosen, setChosen] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const [score, setScore] = useState(0);
  const [hints, setHints] = useState(0);
  const [work, setWork] = useState("");
  const [finished, setFinished] = useState(false);
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setIndex(0);
    setChosen(null);
    setChecked(false);
    setScore(0);
    setHints(0);
    setWork("");
    setFinished(false);
    setMessage("");
    setSaving(false);
  }, [lessonId]);

  function reset() {
    setIndex(0);
    setChosen(null);
    setChecked(false);
    setScore(0);
    setHints(0);
    setWork("");
    setFinished(false);
    setMessage("");
    setSaving(false);
  }

  function check() {
    const current = items[index];

    if (!current || chosen === null || checked) {
      return;
    }

    setChecked(true);

    if (chosen === current.answerIndex) {
      setScore((previous) => previous + 1);
    }
  }

  async function next() {
    if (!lesson || saving || !checked) {
      return;
    }

    if (index < items.length - 1) {
      setIndex((previous) => previous + 1);
      setChosen(null);
      setChecked(false);
      setHints(0);
      setWork("");
      return;
    }

    setSaving(true);

    try {
      const result = await savePractice(
        lesson.id,
        score,
        items.length
      );

      setMessage(
        result.message ||
          (result.ok
            ? "Practice saved successfully."
            : "Progress could not be saved.")
      );
    } catch {
      setMessage(
        "Could not save progress. Please try again later."
      );
    } finally {
      setSaving(false);
      setFinished(true);
    }
  }

  if (
    !lesson ||
    !chapter ||
    !track ||
    items.length !== 20
  ) {
    return (
      <div className="blank-state">
        Practice unavailable.{" "}
        <Link href="/">Return home</Link>
      </div>
    );
  }

  const q = items[index];
  const correct = chosen === q.answerIndex;
  const percent = Math.round(
    (score / items.length) * 100
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
            title: lesson.title,
            href: `/learn/${lesson.id}`,
          },
          {
            title: "Practice",
          },
        ]}
      />

      {finished ? (
        <div className="results-card">
          <span className="results-trophy">
            <Trophy size={43} />
          </span>

          <span className="section-kicker">
            SESSION COMPLETE
          </span>

          <h1>Practice complete!</h1>

          <p>
            You worked through all 20 questions.
            Review your mistakes, then try again
            to improve your score.
          </p>

          <div className="score-display">
            <strong>
              {score}
              <span> / 20</span>
            </strong>

            <span>{percent}% correct</span>
          </div>

          <ProgressBar
            percent={percent}
            color={score >= 14 ? "mint" : "violet"}
            height={12}
          />

          <div className="result-message">
            {score >= 17
              ? "Excellent work! You're building real fluency!"
              : score >= 12
              ? "Great progress. Review the formulas, then try again."
              : "Every attempt counts. Revisit the lesson and use the hints next time."}
          </div>

          {message && (
            <p className="save-message">
              {message}
            </p>
          )}

          <div className="result-actions">
            <button
              type="button"
              className="button button-outline"
              onClick={reset}
            >
              <RotateCcw size={17} />
              Retry all 20
            </button>

            <Link
              className="button button-primary"
              href={`/test/${chapter.id}`}
            >
              Chapter checkpoint
              <ArrowRight size={17} />
            </Link>

            <Link
              className="button button-ghost"
              href={`/learn/${lesson.id}`}
            >
              Back to lesson
            </Link>
          </div>
        </div>
      ) : (
        <div className="practice-wrap">
          <div className="practice-heading">
            <div>
              <span className="section-kicker">
                INTERACTIVE PRACTICE
              </span>

              <h1>{lesson.title}</h1>

              <p>
                Take your time. Hints are here
                when you need them.
              </p>
            </div>

            <Link
              href={`/learn/${lesson.id}`}
              className="button button-ghost"
            >
              <ArrowLeft size={16} />
              Back to lesson
            </Link>
          </div>

          <div className="practice-progress">
            <div>
              <strong>
                Question {index + 1} of {items.length}
              </strong>

              <span>
                {score} correct so far
              </span>
            </div>

            <ProgressBar
              percent={
                ((index + (checked ? 1 : 0)) /
                  items.length) * 100
              }
              height={9}
            />
          </div>

          <div className="question-card">
            <div className="question-topline">
              <span className="question-tag">
                <Target size={15} />
                {q.difficulty}
              </span>

              <span className="question-number">
                {String(index + 1).padStart(2, "0")}
                {" / "}
                {items.length}
              </span>
            </div>

            <h2 className="question-prompt">
              {q.prompt}
            </h2>

            <p className="question-instruction">
              Choose the best answer.
            </p>

            <div
              className="answer-options"
              role="radiogroup"
              aria-label="Answer choices"
            >
              {q.options.map(
                (option, optionIndex) => (
                  <button
                    key={optionIndex}
                    type="button"
                    role="radio"
                    aria-checked={
                      chosen === optionIndex
                    }
                    disabled={checked}
                    onClick={() =>
                      setChosen(optionIndex)
                    }
                    className={[
                      "answer-option",
                      chosen === optionIndex
                        ? "selected"
                        : "",
                      checked &&
                      optionIndex === q.answerIndex
                        ? "right"
                        : "",
                      checked &&
                      chosen === optionIndex &&
                      !correct
                        ? "wrong"
                        : "",
                    ]
                      .filter(Boolean)
                      .join(" ")}
                  >
                    <span className="option-letter">
                      {String.fromCharCode(
                        65 + optionIndex
                      )}
                    </span>

                    <span>{option}</span>

                    {checked &&
                      optionIndex ===
                        q.answerIndex && (
                        <CheckCircle2
                          className="option-feedback"
                          size={21}
                        />
                      )}

                    {checked &&
                      chosen === optionIndex &&
                      !correct && (
                        <XCircle
                          className="option-feedback"
                          size={21}
                        />
                      )}
                  </button>
                )
              )}
            </div>

            {!checked && (
              <div className="hints-section">
                <button
                  type="button"
                  className="hint-trigger"
                  disabled={hints >= 2}
                  onClick={() =>
                    setHints((previous) =>
                      Math.min(2, previous + 1)
                    )
                  }
                >
                  <Lightbulb size={17} />

                  {hints === 0
                    ? "Need a hint?"
                    : hints === 1
                    ? "Show another hint"
                    : "All hints revealed"}
                </button>

                {q.hints
                  .slice(0, hints)
                  .map((hint, hintIndex) => (
                    <div
                      className="hint-box"
                      key={hintIndex}
                    >
                      <strong>
                        Hint {hintIndex + 1}
                      </strong>

                      <p>{hint}</p>
                    </div>
                  ))}
              </div>
            )}

            {checked && (
              <div
                className={`feedback-box ${
                  correct
                    ? "correct"
                    : "incorrect"
                }`}
              >
                <div className="feedback-title">
                  {correct ? (
                    <CheckCircle2 size={22} />
                  ) : (
                    <XCircle size={22} />
                  )}

                  <strong>
                    {correct
                      ? "Exactly right!"
                      : "Good try. Let's work it through."}
                  </strong>
                </div>

                <div className="feedback-steps">
                  <span className="small-overline">
                    STEP-BY-STEP EXPLANATION
                  </span>

                  {q.hints[0] && (
                    <p>
                      <b>1.</b> {q.hints[0]}
                    </p>
                  )}

                  {q.explanation.map(
                    (line, stepIndex) => (
                      <p key={stepIndex}>
                        <b>
                          {stepIndex + 2}.
                        </b>{" "}
                        {line}
                      </p>
                    )
                  )}

                  <p className="correct-answer">
                    Correct answer:{" "}
                    {q.options[q.answerIndex]}
                  </p>
                </div>
              </div>
            )}

            <div className="question-footer">
              <span>
                {checked
                  ? "Great job taking this step!"
                  : "No timer. Just you and the math."}
              </span>

              {!checked ? (
                <button
                  type="button"
                  className="button button-primary"
                  disabled={chosen === null}
                  onClick={check}
                >
                  Check answer
                  <ArrowRight size={18} />
                </button>
              ) : (
                <button
                  type="button"
                  className="button button-primary"
                  disabled={saving}
                  onClick={next}
                >
                  {saving
                    ? "Saving..."
                    : index ===
                      items.length - 1
                    ? "Finish practice"
                    : "Next question"}

                  <ArrowRight size={18} />
                </button>
              )}
            </div>
          </div>

          <div className="scratchpad">
            <div>
              <Sparkles size={19} />

              <strong>
                Show your work
              </strong>

              <span>
                Private scratchpad · not submitted
              </span>
            </div>

            <textarea
              aria-label="Your scratchpad"
              value={work}
              onChange={(event) =>
                setWork(event.target.value)
              }
              placeholder="Type your reasoning, equations, or notes here. This is just for you."
              rows={3}
            />
          </div>
        </div>
      )}
    </div>
  );
}
