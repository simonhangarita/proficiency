from openai import OpenAI
import spacy
import pandas as pd
from sqlalchemy import create_engine,Column,String,Text,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#We define the OpenAI and spacy.load entities
client=OpenAI()
nlp = spacy.load("en_core_web_sm")
#We initialize the base and engine for the database
engine = create_engine("sqlite:///users.db")
Base = declarative_base()
class Request(Base):
    __tablename__='requests'
    id=Column(Integer,primary_key=True,index=True)
    date=Column(String,nullable=False)
    user=Column(String,nullable=False)
    text=Column(String,nullable=False)
    sentiment=Column(String,nullable=False)
    priority=Column(String,nullable=False)
def processing_file(file:str)->pd.Dataframe:
    """
    We use pandas to convert the file whether is a json file or csv to a pandas dataframe to process the information
    Args:
        file: name of the file that we need to process
    Returns:
        df:dataframe with the information that comes from the csv or json file
    """
    try:
        df = pd.read_json(file)
    except ValueError:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return pd.DataFrame()
    return df

def text_classification(text:str)->str:
    """
    We receive a text and we have to classify it as a negative, neutral or positive in order to prioritize urgencies
    Args: 
        text(str): Text of a client that we need to classify
    Returns:
        classification(str): We return one of the following classifications for the text positive, neutral or negative or error in case we
        couldn't return the correct value
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a healthcare assistant. Classify text as: positive, negative, or neutral. Return ONLY the word."},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return response.choices[0].message.content.lower().strip()
    except Exception as e:
        return "Error"
def process_sentiment(text:str,sentiment:str)->str:
    if sentiment=='negative':

        doc = nlp(text)

        key_words = ["pain", "ache", "hurt", "excruciating","urgency","waiting","long","time","accident"]

        if any(token.lemma_ in key_words for token in doc):
            return 'high'
        return 'medium'
    else:
        return 'low'

def main():
    file=input("Insert the file location you are going to use: ")
    df=processing_file(file)
    #We open the session to insert the values in the database
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    if not df.empty:
        try:
            df['sentiment']=df.apply(lambda x:text_classification(x['text']),axis=1)
            df['priority']=df.apply(lambda x:process_sentiment(x['text'],x['sentiment']),axis=1)
            try:
                requests=[Request(
                                date=row["date"],
                                user=row['user']
                                ,text=row['text'],
                                sentiment=['sentiment'],
                                priority=row['priority'])
                            for row in df.to_dict('records')]
                try:
                    session.add_all(requests)
                    session.commit()
                    print("The registers had been inserted!")
                finally:
                    session.close()
            except  Exception as e:
                print("One of the fields date or user  was not provided in the file")
        except Exception as e:
            print("There is no text field in the file you provided")


if __name__=='__main__':
    main()

