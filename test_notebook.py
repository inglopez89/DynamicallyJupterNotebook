import pandas as pd
from io import open
import json
import sqlite3

class Testnotebook:
    """"
    A class represent the notebook test
    ...
    Attributes
    ----------
    params: str
        source with the file json with params for create the notebook.
    """
    def __init__(self, params):
        self.params = params

    def __read_params(self):
        try:
            with open(self.params) as file:
                parameters = json.load(file)
            area = parameters['area']
            db = parameters['DB']
            questions = parameters['questions']
            path_notebook = parameters['path_notebook']
            return area, db, questions, path_notebook
        except Exception as e:
            print('An error has occurred: ', e)

    def __read_questions(self, db):
        """
        A method for connect sqlite and read the questions
        ...
        Attributes
        -----------
        db: str
            Source of database sqlite
        return: df
            return the dataframe with the questions
        """
        try:
            conn = sqlite3.connect(db)
            df_head = pd.read_sql_query('select * from head', conn)
            df_type = pd.read_sql_query('select * from type', conn)
            df_questions = pd.read_sql_query('select * from questions', conn)
            conn.close()
            test = df_head.merge(df_type, on='id_head', how='left')
            test = test.merge(df_questions, on='id_category', how='left')
            test = test[['Desc_test', 'Subject', 'type',
                         'load_script', 'head', 'img', 'question', 'level']]
            return test
        except Exception as e:
            print('An error has been occurred when read questions', e)

    def __iter_df(self, df):
        """
        A Method for iter dataframe and create an list according to the format for Jupyter notebook, with
        the cells with informations for questions.
        Attributes
        -----------
         df: df
            Is a dataframe with the questions
        return: list
            Return the list of about the cells created according to the jupyter notebook format.
        """
        try:
            listq = []
            for index, row in df.iterrows():
                listq.append({"cell_type": "markdown", "metadata": {},
                              "source": [str(row[6]).replace("['", '').replace("']", '')]})
                listq.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                              "source": [""]})
            return listq
        except Exception as e:
            print('An error has occurred when try iter:', e)

    def __random_questions(self, df, q_type, level, n_question):
        """
        A method for select
        df: df
            this is a dataframe with the questions for random selection
        q_type: str
            Is a type of questions example: program, sql ..
        level: str
            this is a level for question selection, basic, intermediate and advanced
        n_question: int
            This is a number of questions that wants select
        return: list
            Return a list with random questions
        """
        try:
            df_filter = df[(df['type'] == q_type) & (df['level'] == level)]
            df_filter = df_filter.sample(n=n_question)
            iter_questions = self.__iter_df(df_filter)
            return iter_questions
        except Exception as e:
            print('An error has occurred when try create random questions: ', e)

    def create_notebook(self):
        """
        A method for create the jupyter notebook with random questions.
        """
        try:
            area, db, questions, path_notebook = self.__read_params()
            df_questions = self.__read_questions(db)
            cell_array = []
            df_questions = df_questions[df_questions['Desc_test'] == area]

            # Load greet
            cell_array.append({"cell_type": "markdown", "metadata": {},
                               "source": [str(df_questions.Subject.unique()).replace("['", '').replace("']", '')]})
            if df_questions.load_script.nunique() > 0:
                cell_array.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                              "source": [str(df_questions.load_script.unique()).replace("['", '').replace("']", '')]})
            # Load cells with random questions
            for q_list in questions:
                q_type = q_list["type"]
                q_level = dict(q_list["q_level"])
                for k, v in q_level.items():
                    cell_array.extend(self.__random_questions(df_questions, q_type, k, v))

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
            notebook = open(path_notebook, 'w')
            notebook.write(json.dumps(cells))
            notebook.close()

        except Exception as e:
            print('An error has occurred when notebook was been created: ', e)

if __name__ == '__main__':
    file_test = Testnotebook('/home/clopez/Documents/Project_test/params.json')
    file_test.create_notebook()
