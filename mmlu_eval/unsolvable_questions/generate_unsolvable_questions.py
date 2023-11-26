"""
To represent the setup for "Unsolvable Question Generation via Constraint-violated Perturbations" using Pydantic, 
we can create a Pydantic model that represents the parameters of the structural design question and 
then define constraints for those parameters. 
"""

from pydantic import BaseModel, validator, root_validator, ValidationError
from math import floor

from pydantic import BaseModel, ValidationError
from math import floor


class StructuralDesignQuestion(BaseModel):
    WIDTH: int
    DEPTH: int
    DIAMETER: int
    SPACING: int

    @validator("DEPTH", pre=True, always=True)
    def depth_greater_than_diameter(cls, depth, values):
        diameter = values.get('DIAMETER')
        if diameter and depth <= diameter:
            raise ValueError("DEPTH must be greater than DIAMETER")
        return depth

    @validator("WIDTH", pre=True, always=True)
    def width_greater_than_spacing(cls, width, values):
        spacing = values.get('SPACING')
        if spacing and width <= spacing:
            raise ValueError("WIDTH must be greater than SPACING")
        return width

    @root_validator(pre=True)
    def check_width_and_diameter(cls, values):
        width = values.get('WIDTH')
        diameter = values.get('DIAMETER')
        spacing = values.get('SPACING')
        if width and diameter and spacing:
            num_spaces = floor((width - diameter) / spacing)
            if num_spaces < 1:
                raise ValueError("WIDTH must be greater than DIAMETER given the SPACING")
        return values
    
    def break_depth_diameter_constraint(self):
        """Break the DEPTH > DIAMETER constraint."""
        self.DEPTH = self.DIAMETER - 5  # Making depth 5 units less than diameter for demonstration
        return self.generate_question()

    def break_width_spacing_constraint(self):
        """Break the WIDTH > SPACING constraint."""
        self.WIDTH = self.SPACING - 10  # Making width 10 units less than spacing for demonstration
        return self.generate_question()

    def break_width_diameter_constraint(self):
        """Break the WIDTH > DIAMETER given the SPACING constraint."""
        self.WIDTH = (self.SPACING + self.DIAMETER) - 20  # Adjusting width to break the constraint
        return self.generate_question()
    

    def generate_question(self):
        return f"How many bars are required for a {self.WIDTH} wide x {self.DEPTH} deep section with N{self.DIAMETER}-{self.SPACING} c/c and 40MPa concrete?"
 

    def generate_unsolvable_question(self):
        unsolvable_questions = []
        # Breaking the DEPTH > DIAMETER constraint
        unsolvable_questions.append(self.break_depth_diameter_constraint())
        # Breaking the WIDTH > SPACING constraint
        unsolvable_questions.append(self.break_width_spacing_constraint())
        # Breaking the WIDTH > DIAMETER given the SPACING constraint
        unsolvable_questions.append(self.break_width_diameter_constraint())
        return unsolvable_questions

# Example Usage
try:
    # Example Usage
    generator = StructuralDesignQuestion(WIDTH=1000, DEPTH=350, DIAMETER=24, SPACING=145)
    unsolvable_questions = generator.generate_unsolvable_question()
    print(unsolvable_questions)
except ValidationError as e:
    print(e)

{"input":[{"role":"system","content":"You are UnsolvableGPT. You will be provided a question and some context for the question. Using only the context to answer the question determine if it is \"Solveable\" or \"Unsolveable\". Respond with only one word without punctuation, either: \"Solveable\": The submitted question is solveable with the context provided alongside it and no other outside information OR \"Unsolveable\": The submitted question is unsolveable with the context provided alongside it. There is not enough context to answer the question. Remember, only answer with \"Solveable\" OR \"Unsolveable\", do not include anything else."},
          {"role":"user","content":f"Question: {question}\n Context: {context}"}]}



