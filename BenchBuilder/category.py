# Tag structure
# - category_tag
#     - criteria_v0.1
#         - specificity
#         - ...
#     - math_v0.1
#         - math
#     - if_v0.1
#         - if
#         - score
import ast
import re
import os
import json


class Category:
    def __init__(self):
        pass

    @staticmethod
    def create_category(name):
        if name == "criteria_v0.1":
            return CategoryHardPrompt()
        raise Exception(f"Category name is incorrect: {name}")

    def post_process(self):
        pass


class CategoryHardPrompt(Category):
    def __init__(self):
        super().__init__()
        self.name_tag = "criteria_v0.1"
        self.pattern = re.compile(r"(\[[1234567](?:\,\s[1234567])*\])")
        asssets_folder = os.path.join(os.path.dirname(__file__), 'asssets')

        with open(os.path.join(asssets_folder, "shema.json"), 'r', encoding='utf-8') as file:
            self.output_schema = json.load(file)

        with open(os.path.join(asssets_folder, "prompt.txt"), 'r', encoding='utf-8') as file:
            self.sys_prompt = file.read()
        self.content_prompt = """Do not add anything additional to your answer.
--- Input:
{
    "prompt": {{prompt}}
}
--- Output:"""

        self.tags = {
            1: "specificity",
            2: "domain_knowledge",
            3: "complexity",
            4: "problem_solving",
            5: "creativity",
            6: "technical_accuracy",
            7: "real_world",
        }

    def get_score(self, judgment):
        matches = self.pattern.findall(judgment)
        matches = [m for m in matches if m != ""]
        if len(set(matches)) == 0:
            return ['No Match']
        elif len(set(matches)) == 1:
            try:
                return ast.literal_eval(matches[0])
            except SyntaxError:
                print(matches[0])
                return ['Syntax Error']
        else:
            return ['Multiple Match']

    def pre_process(self, prompt):
        conv = [{"role": "system", "content": self.sys_prompt}]
        conv.append({"role": "user", "content": self.content_prompt.format(prompt=prompt)})
        return conv

    def post_process(self, judgment):
        if judgment is None:
            return {}
        result = json.loads(judgment)
        return result