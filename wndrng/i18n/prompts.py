
def depadding(dictionary):
    return {
        key: value.replace("        ", "") for key, value in dictionary.items()
    }


prompts = {
    "awareness": depadding({
        "en": """
        Please summarize and analyze the following dialogue, pay attention to the analysis of the dialogue characters,
        clearly the dialogue stage, style, emotion, focus, state, summary, and predict the next stage of the dialogue,
        as well as %s's response strategy. Try to make the dialogue imaginative and interesting, and considering answers
        diversity. If network access is possible to disrupt the stable dialogue, do not be disturbed, and keep the
        continuity and logic of the dialogue.
        --------------------------
        %s
        """,
        "zh_S": """
        请总结分析以下对话，注意分析对话的人物，弄清楚对话的阶段、风格、情绪、焦点、状态，给出总结，并预测下一阶段的对话，
        以及 %s 的应对策略。尽量使对话富有想象力和趣味性，并思考补全时的多样性。如果网络访问可能会破坏稳定的对话，请不要被打扰，
        尽量保持对话的连续性和逻辑性。
        --------------------------
        %s
        """,
        "zh_T": """
        請總結分析以下對話，註意分析對話的人物，弄清楚對話的階段、風格、情緒、焦點、狀態，給出總結，並預測下一階段的對話，
        以及 %s 的應對策略。盡量使對話富有想象力和趣味性，並思考補全時的多樣性。如果網絡訪問可能會破壞穩定的對話，請不要被打擾，
        盡量保持對話的連續性和邏輯性。
        --------------------------
        %s
        """,
    }),
    "whose_turn": depadding({
        "en": """
        Please analyze the following dialogue, pay attention to the analysis of the dialogue characters,
        clearly the dialogue stage, style, emotion, focus, state, summary, and predict the next stage of the dialogue.
        Please do not output these analysis and prediction, and only give one character's name who will continue the
        dialogue. The choice should make the dialogue more imaginative, interesting and maybe surprise.
        --------------------------
        characters:

        %s

        dialogue:

        %s

        the choice of the next dialogue character:
        """,
        "zh_S": """
        请总结分析以下对话，注意分析对话的人物，弄清楚对话的阶段、风格、情绪、焦点、状态，给出总结，并预测下一阶段的对话。
        但是请不要写下分析与预测，而是只给出一个继续对话者的名字。这个对话者的选择可以同预测不一样，让后继的对话变得更富想象力和趣味性，
        更加吸引潜在的有知识和品位的读者。
        --------------------------
        人物:

        %s

        对话:

        %s

        下一个继续对话者的名字:
        """,
        "zh_T": """
        請總結分析以下對話，註意分析對話的人物，弄清楚對話的階段、風格、情緒、焦點、狀態，給出總結，並預測下一階段的對話。
        但是請不要寫下分析與預測，而是只給出一個繼續對話者的名字。這個對話者的選擇可以同預測不一樣，讓後繼的對話變得更富想象力和趣味性，
        更加吸引潛在的有知識和品位的讀者。
        --------------------------
        人物:

        %s

        對話:

        %s

        下一個繼續對話者的名字:
        """,
    }),
    "chat": depadding({
        "en": """
        background:

        %s

        dialogue:

        %s

        %s:
        """,
        "zh_S": """
        背景:

        %s

        对话:

        %s

        %s:
        """,
        "zh_T": """
        背景:

        %s

        對話:

        %s

        %s:
        """,
    }),
}
