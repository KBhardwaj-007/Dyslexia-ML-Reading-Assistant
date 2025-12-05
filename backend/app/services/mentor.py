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

    message = (
        f"Hey {payload.learner_name}, I noticed your pace is {payload.pace_wpm:.0f} wpm "
        f"with accuracy {payload.accuracy:.2f}. {focus_note}"
    )

    summary = [
        f"Accuracy trending at {payload.accuracy:.2f} ({gains:+} pts vs baseline).",
        f"Focus score {payload.focus_score:.2f}; streak {payload.streak_minutes:.1f} min.",
    ]

    next_actions = [
        "Replay tricky words with syllable highlights",
        "Do a 2-minute breathing break to reset focus",
        "Try the next passage one level up if you feel ready",
    ]

    return MentorResponse(persona=persona, message=message, summary=summary, next_actions=next_actions)
