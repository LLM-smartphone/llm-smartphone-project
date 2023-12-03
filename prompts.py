class HistoryPrompt:
    def __init__(self, task_desc, func_desc):
        self.previous_response = []
        self.task_desc = task_desc
        self.func_desc = func_desc

    def append_response(self, response):
        self.previous_response.append(response)
        if len(self.previous_response) > 1: # keep the history short
            self.previous_response.pop(0)
    
    def generate_prompt_with_history(self, ui_list):
        prompt = f"Here is a screenshot of a smartphone. Some useful UI elements are bounded in colorful boxes with an ID number on the top-left corner of the box. The ID number has the same color with the corresponding bounding box. Instead of guessing the ID numbers sequentially, always read it from the image. You are a professional smartphone user. Your task is: {self.task_desc}. Based on the current screenshot, what will you do next? Briefly summarize what's in the screenshot, and what's your next action. Also, for each UI element, describe what does it do, starting with the ID number shown in the box. In the end of your output, put a Python function call representing your action in a code block. The available functions include {self.func_desc} Note: from the home screen, `scroll_down()` can show all apps."

        content_desc = dict()
        for i, element in enumerate(ui_list):
            desc = element.map['content-desc']
            if len(desc) > 0:
                content_desc[i] = desc
        if len(content_desc) > 0: # at least 1 view has content-desc
            prompt += "\n"
            prompt += "Hint: some UI elements have the following content description, you should utilize it to understand the screenshot better:"
            for k in sorted(content_desc.keys()):
                prompt += f"\nID {k}: {content_desc[k]}"

        if len(self.previous_response) == 0:
            return prompt
    
        # has previous responses
        prompt += "\n"
        prompt += "The following paragraph between curly brackets contains your previous UI descriptions and actions in chronological order, separeted with dashes (---). Examine your previous actions and compare with the current screenshot. Answer the following questions: What's your last action? Is the current UI state as expected, based on your previous actions? If it's not as expected, then your previous thought is wrong and you must try a different action. All action functions are registered, so retrying won't help. Consider to scroll the screen and explore more contents when your action failed."
        
        prompt += "\n{\n"
        for i, each in enumerate(self.previous_response):
            prompt += each
            prompt += "\n---\n"
        prompt += "}"
        return prompt

            