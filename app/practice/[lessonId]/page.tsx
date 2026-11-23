
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
  }, [lessonId]);

  if (!lesson || items.length !== 20) {
    return (
      <div className="blank-state">
        Practice unavailable.{" "}
        <Link href="/">Return home</Link>
      </div>
    );
  }

  const chapter = chapterById(lesson.chapterId);

  if (!chapter) {
    return (
      <div className="blank-state">
        Chapter unavailable.{" "}
        <Link href="/">Return home</Link>
      </div>
    );
  }

  const track = trackById(chapter.trackId);

  if (!track) {
    return (
      <div className="blank-state">
        Track unavailable.{" "}
        <Link href="/">Return home</Link>
      </div>
    );
  }

  const q = items[index];
  const correct = chosen === q.answerIndex;

  function reset() {
    setIndex(0);
    setChosen(null);
    setChecked(false);
    setScore(0);
    setHints(0);
    setWork("");
    setFinished(false);
    setMessage("");
  }

  function check() {
    if (chosen === null || checked) return;

    setChecked(true);

    if (correct) {
      setScore((s) => s + 1);
    }
  }

  async function next() {
    if (!lesson) return;

    if (index < items.length - 1) {
      setIndex((i) => i + 1);
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
      setMessage("Progress could not be saved.");
    } finally {
      setSaving(false);
      setFinished(true);
    }
  }

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
            The best way to improve is to review
            your mistakes and try again.
          </p>

          <div className="score-display">
            <strong>
              {score}
              <span> / 20</span>
            </strong>

            <span>
              {Math.round((score / 20) * 100)}% correct
            </span>
          </div>

          <ProgressBar
            percent={score / 20 * 100}
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
            <div className="save-message">
              {message}
            </div>
          )}

          <div className="result-actions">
            <button
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

              <span>{score} correct so far</span>
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

            <div
              className="question-options"
              role="radiogroup"
              aria-label="Choose an answer"
            >
              {q.options.map((option, i) => (
                <button
                  key={i}
                  type="button"
                  role="radio"
                  aria-checked={chosen === i}
                  onClick={() => {
                    if (!checked) setChosen(i);
                  }}
                  disabled={checked}
                  className={
                    `answer-option ${
                      chosen === i ? "selected" : ""
                    } ${
                      checked && i === q.answerIndex
                        ? "right"
                        : ""
                    } ${
                      checked &&
                      chosen === i &&
                      !correct
                        ? "wrong"
                        : ""
                    }`
                  }
                >
                  <span className="option-letter">
                    {String.fromCharCode(65 + i)}
                  </span>

                  <span>{option}</span>

                  {checked &&
                    i === q.answerIndex && (
                      <CheckCircle2
                        size={21}
                        className="option-feedback"
                      />
                    )}
                </button>
              ))}
            </div>

            {!checked && (
              <div className="hints-section">
                <button
                  type="button"
                  className="hint-trigger"
                  onClick={() =>
                    setHints((x) => Math.min(2, x + 1))
                  }
                  disabled={hints >= 2}
                >
                  <Lightbulb size={17} />

                  {hints === 0
                    ? "Need a hint?"
                    : hints === 1
                    ? "Show another hint"
                    : "All hints revealed"}
                </button>

                {q.hints.slice(0, hints).map((h, i) => (
                  <div className="hint-box" key={i}>
                    <strong>Hint {i + 1}</strong>
                    <p>{h}</p>
                  </div>
                ))}
              </div>
            )}

            {checked && (
              <div
                className={`feedback-box ${
                  correct ? "correct" : "incorrect"
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
                      : "Good try—let's work it through."}
                  </strong>
                </div>

                <div className="feedback-steps">
                  <span className="small-overline">
                    STEP-BY-STEP EXPLANATION
                  </span>

                  {q.hints[0] && <p>{q.hints[0]}</p>}
                  {q.hints[1] && <p>{q.hints[1]}</p>}

                  {q.explanation
                    .map((line, i) => (
                      <p key={i}>
                        <b>Step {i + 1}:</b> {line}
                      </p>
                    ))}

                  <p>
                    <strong>Correct answer:</strong>{" "}
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
                    : index === 19
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

              <strong>Show your work</strong>
            </div>

            <strong>
              Private scratchpad · not submitted
            </strong>

            <textarea
              aria-label="Your scratchpad"
              value={work}
              onChange={(e) =>
                setWork(e.target.value)
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
