import pandas as pd
from io import open
import json

class Testnotebook:
    """"
    A class represent the notebook test
    ...
    Attributes
    ----------
    category: str
        Represent the category for select the questions
    rutaTest: str
        Represent the source in this case excel file
    """
    def __init__(self, category, rutaTest, questions_number):
        self.category = category
        self.rutaTest = rutaTest
        self.questions_number = questions_number

    def __read_questions(self):
        try:
            head = pd.read_excel(self.rutaTest, header=0, sheet_name='Head')
            category = pd.read_excel(self.rutaTest, header=0, sheet_name='head_type')
            questions = pd.read_excel(self.rutaTest, header=0, sheet_name='Questions')
            test = head.merge(category, on='id_head', how='left')
            test = test.merge(questions, on='id_category', how='left')
            test = test[['Desc_test', 'Subject', 'des_category',
                         'load_script', 'head', 'img', 'question', 'level']]
            #print(test)
            return test
        except Exception as e:
            print('An error has been occurred', e)

    def __iter_df(self, df):
        try:
            listq = []
            for index, row in df.iterrows():
                listq.append({"cell_type": "markdown", "metadata": {},
                              "source": [str(row[6]).replace("['", '').replace("']", '')]})
                listq.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                              "source": [""]})
            return listq
        except Exception as e:
            print('An error has occurred when try iter:',e)

    def __random_questions(self):
        try:
            pd_questions = self.__read_questions()
            pd_program = pd_questions[pd_questions['des_category'] == 'Program']
            pd_sql = pd_questions[pd_questions['des_category'] == 'Sql']
            pd_program = pd_program.sample(n=round(self.questions_number / 2)-1)
            pd_sql = pd_sql.sample(n=round(self.questions_number / 2))
            questions = self.__iter_df(pd_program)
            questions.extend(self.__iter_df(pd_sql))
            return questions
        except Exception as e:
            print('An error has occurred when try create random questions: ', e)

    def create_notebook(self):
        try:
            questions = self.__read_questions()
            cell_array = []
            if self.category == 'your category here':# parameter for select category for questions
                questions = questions[questions['Desc_test'] == 'select category that you add in the excel file']
                # Load greet
                cell_array.append({"cell_type": "markdown", "metadata": {},
                                   "source": [str(questions.Subject.unique()).replace("['", '').replace("']", '')]})
                # Load cells with random questions
                cell_array.extend(self.__random_questions())
                cells = dict({"cells": cell_array})
                #Create Metadata for Jupyter notebook
                metadata = dict({"metadata": {"kernelspec": {
                            "display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {
                            "codemirror_mode": {"name": "ipython", "version": 3},
                            "file_extension": ".py", "mimetype": "text/x-python", "name": "python",
                            "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.6.5"
                                        }
                                    },
                            "nbformat": 4,
                            "nbformat_minor": 2
                                })
                cells.update(metadata)
                # Create file Jupyter notebook for test
                notebook = open('your route/interview.ipynb', 'w')
                notebook.write(json.dumps(cells))
                notebook.close()
        except Exception as e:
            print('An error has occurred when notebook was been created: ', e)

if __name__ == '__main__':
    file_test = Testnotebook('your category created', 'your route with questions/BD_test.xls', 7) # the number is a number of questions that you want in your notebook
    file_test.create_notebook()
