from ..models import MentorRequest, MentorResponse


def craft_response(payload: MentorRequest) -> MentorResponse:
    tone = payload.tone if payload.tone in {"friendly", "teacher", "calm"} else "friendly"
    persona = {
        "friendly": "Sunny Coach",
        "teacher": "Ms. Rivera",
        "calm": "Guide Kai",
    }[tone]

    gains = round((payload.accuracy - 0.6) * 100)
    focus_note = "Great focus streak!" if payload.focus_score >= 0.7 else "Let's try a mini-break then continue."
    fatigue_note = "We can stretch soon." if payload.fatigue_score > 0.45 else "Energy looks good."
    distraction_note = "I saw a distraction spike; let's reset breath." if payload.distraction_flag else "Keep the same pace."

    message = (
        f"Hey {payload.learner_name}, pace {payload.pace_wpm:.0f} wpm, accuracy {payload.accuracy:.2f}, level {payload.level}. "
        f"{focus_note} {fatigue_note} {distraction_note}"
    )

    summary = [
        f"Accuracy {payload.accuracy:.2f} ({gains:+} pts vs baseline).",
        f"Focus {payload.focus_score:.2f}; fatigue {payload.fatigue_score:.2f}; streak {payload.streak_minutes:.1f} min.",
        f"Current level {payload.level}.",
    ]

    next_actions = [
        "Replay tricky words with syllable highlights",
        "Take a 2-minute breathing break if you feel tired",
        "Advance one level when focus stays above 0.7",
    ]

    return MentorResponse(persona=persona, message=message, summary=summary, next_actions=next_actions)
