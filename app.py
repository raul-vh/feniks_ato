import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import duckdb
import plotly.express as px
import random
import string

def connect_to_google_docs():
    """
    Connect to google docs sheet with survey results using duckdb.
    Returns dataframe.
    """
    load_dotenv()
    url = os.getenv('GOOGLESHEETS_URL')
    try:
        df = duckdb.sql(
            f"SELECT * FROM read_csv_auto('{url}',ignore_errors=1)").df()
        df = df.drop(labels=['Timestamp', 'Naam', 'Telefoonnummer', '[FRD Response ID] DO NOT REMOVE'], axis=1)
    except Exception as exeption:
        print(str(exeption))
    return df

def histogram(df, column_name, laag, hoog):
    """
    Prints histogram for specific column name
    """
    fig = px.histogram(df, x=column_name, title=column_name, nbins=10, text_auto=True)
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(range=[0.5, 5.5], 
                    ticktext=[laag, "", "", "", hoog],
                    tickvals=[1, 2, 3, 4, 5])
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    return

def pie_chart(df, column_name):
    """
    Prints pie chart for specific column name
    """
    fig = px.pie(df, names=column_name, title=column_name)
    fig.update_traces(textposition='inside', textinfo='label+percent')
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    return

def bar_chart(df, column_name, scale_meaning):
    """
    Prints bar chart for specific column name
    """
    fig = px.bar(df[column_name].value_counts(), 
                y="count", 
                title=column_name,
                text_auto=True)
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(range=[0.5, 5.5], 
                    ticktext=scale_meaning,
                    tickvals=[1, 2, 3, 4, 5])
    st.plotly_chart(fig, use_container_width=True)
    return

if __name__ == "__main__":
    df = connect_to_google_docs()

    st.set_page_config(page_title="Atleten Tevredenheids Onderzoek",
                       page_icon=":bar_chart:",
                       layout="centered")

    st.sidebar.header("Filter hier op trainingsgroep:")

    trainingsgroep = st.sidebar.multiselect(
        "Selecteer trainingsgroep:",
        options=df["In welke trainingsgroep train jij?"].unique(),
        default=df["In welke trainingsgroep train jij?"].unique(),
        )

    df_selection = df.query(
        "`In welke trainingsgroep train jij?` == @trainingsgroep"
    )
    st.markdown("""
                # Atleten Tevredenheids Onderzoek Q1 2024
                Beste Feniks Atleten,\n\n
                Welkom bij de resultaten van het atleten tevredenheids onderzoek.\n\n
                **Filter linksboven op trainingsgroep** \n\n
                ---
                """)
    voortgang = pd.DataFrame(df_selection["In welke trainingsgroep train jij?"].value_counts())
    voortgang = voortgang.rename(columns={"count": "reacties", "In welke trainingsgroep train jij?": "Trainingsgroep"})
    voortgang["aantal atleten op ledenlijst"] = [pd.NA for i in range(len(voortgang))]
    voortgang.index.rename("Trainingsgroep", inplace=True)
    st.write(voortgang)
    selected = option_menu(
        menu_title=None,
        options=["Algemene vragen", "Trainingen Algemeen", "De trainers", "Groepssfeer",
                 "De oraganisatie van de trainingen", "Persoonlijke ontwikkeling", "Wedstrijden", "Verbeterpunten"],
        default_index=0,
        orientation="horizontal",
        icons=["", "", "", "", "", "", ""]
    )
    if selected == "Algemene vragen":
        st.markdown("""
                    ---\n\n
                    ## 1. Algemene vragen
                    """)
        pie_chart(df_selection, "Hoe vaak in de week train je gemiddeld in deze trainingsgroep?")
        bar_chart(df_selection, "In hoeverre train je wedstrijdgericht vs recreatiegericht?", ["Wedstrijdgericht", "","", "","Recreatiegericht"])
    
    elif selected == "Trainingen Algemeen":
        st.markdown("""
                    ---\n\n
                    ## 2. Trainingen Algemeen
                    """)
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            bar_chart(df_selection, "Ik vind de trainingen: leuk", ["Niet Leuk","","","","Leuk"])
            bar_chart(df_selection, "Ik vind de trainingen: vermakelijk", ["Niet vervelend","","","","Vervelend"])
        with col2:
            bar_chart(df_selection, "Ik vind de trainingen: gezellig", ["Niet gezellig","","","","Gezellig"])
            bar_chart(df_selection, "Ik vind de trainingen: uitdagend", ["Niet uitdagend","","","","Uitdagend"])
        bar_chart(df_selection, "In hoeverre zou je trainen bij Feniks aanraden aan een vriend of famillielid?", ["Zeer onwaarschijnlijk", "Onwaarschijnlijk", "Neutraal", "Waarschijnlijk", "Zeer waarschijnlijk"])
    
    elif selected == "De trainers":
        st.markdown("""
                    ---\n\n
                    ## 3. De trainers
                    """)
        bar_chart(df_selection, "Wat de trainer zegt zorgt bij mij voor:", ["Demotivatie","","","","Motivatie"])
        bar_chart(df_selection, "De trainer zegt soms dingen waardoor ik mij onprettig voel.", ["Nooit","","","","Vaak"])
        bar_chart(df_selection, "Ik durf de trainer om hulp te vragen als ik dat nodig heb.", ["Nooit","","","","Altijd"])
        bar_chart(df_selection, "De trainer luistert naar mij als ik iets kwijt wil.", ["Nooit","","","","Altijd"])
        bar_chart(df_selection, "De trainer neemt mij en mening serieus op momenten dat dat voor mij nodig is.", ["Nooit","","","","Altijd"])
        bar_chart(df_selection, "De trainer komt na wat hij/zij belooft.", ["Nooit","","","","Altijd"])
   
    elif selected == "Groepssfeer":
        st.markdown("""
                    ---\n\n
                    ## 4. Groepssfeer
                    """)
        bar_chart(df_selection, "In de groep voel ik mij:", ["Onveilig","","","","Veilig"])
        bar_chart(df_selection, "Ik voel mij eenzaam in de groep.", ["Nooit","","","","Vaak"])
        bar_chart(df_selection, "De sfeer in de groep is:", ["Onprettig","","","","Prettig"])
        bar_chart(df_selection, "Er wordt gepest in de groep.", ["Nooit","","","","Vaak"])
        bar_chart(df_selection, "Er wordt gelachen in de groep.\n(positief, dus niet uitgelachen)", ["Nooit","","","","Altijd"])
    elif selected == "De oraganisatie van de trainingen":
        st.markdown("""
                    ---\n\n
                    ## 5. De oraganisatie van de trainingen
                    """)
        bar_chart(df_selection, "De training begint altijd op tijd.", ["Nooit","","","","Altijd"])
        bar_chart(df_selection, "De trainer is op tijd aanwezig.", ["Nooit","","","","Altijd"])
        bar_chart(df_selection, "De trainingen vallen regelmatig uit.", ["Nooit","","","","Vaak"])
        bar_chart(df_selection, "De indeling van de trainingen is:\nLangdradig = lange uitleg/tussen onderdelen door lang wachten/dezelfde oefening veel herhalen\nVlot = korte, maar duidelijke uitleg/ snel wisselen van onderdelen/dezelfde oefening niet te lang uitvoeren", ["Langdradig","","","","Vlot"])
        bar_chart(df_selection, "Ik word op tijd en duidelijk geïnformeerd over de planning en wijzigingen van de training.", ["Zeer oneens", "Oneens", "Neutraal", "Eens", "Zeer eens"])
    
    elif selected == "Persoonlijke ontwikkeling":
        st.markdown("""
                    ---\n\n
                    ## 6. Persoonlijke ontwikkeling
                    """)
        bar_chart(df_selection, "Ik word (van tevoren) geïnformeerd over wat het doel van de training is en hoe dit bijdraagt aan mijn verdere ontwikkeling.", ["Zeer oneens", "Oneens", "Neutraal", "Eens", "Zeer eens"])
        bar_chart(df_selection, "Ik ben tevreden over de (technische) inhoud van de trainingen.", ["Zeer oneens", "Oneens", "Neutraal", "Eens", "Zeer eens"])
        bar_chart(df_selection, "Ik heb het gevoel dat de gekozen oefeningen mij beter maken als atleet.", ["Zeer oneens", "Oneens", "Neutraal", "Eens", "Zeer eens"])
        pie_chart(df_selection, "Op welk vlak wil jij je ontwikkelen?")

        test = df_selection["Bij onderdeel specifiek, op welke onderdelen?"]
        test = test.str.split(', ')
        test = test.explode("Bij onderdeel specifiek, op welke onderdelen?")
        value_counts = test.value_counts()
        fig = px.bar(value_counts, x=value_counts.index, y=value_counts, text_auto=True, title="Bij onderdeel specifiek, op welke onderdelen?")
        st.plotly_chart(fig, use_container_width=True)

    elif selected == "Wedstrijden":
        st.markdown("""
                    ---\n\n
                    ## 7. Wedstrijden
                    """)
        bar_chart(df_selection, "Ik word voldoende gestimuleerd om mee te doen aan wedstrijden.", ["Zeer oneens", "Oneens", "Neutraal", "Eens", "Zeer eens"])
        bar_chart(df_selection, "Mijn trainer is aanwezig bij mijn belangrijkste wedstrijden.", ["Nooit", "", "", "", "Altijd"])
        pie_chart(df_selection, "Mijn trainer coacht mij op wedstrijden (of helpt mij op een andere manier om goed voorbereid te zijn op de wedstrijden, ook als hij/zij niet aanwezig kan zijn)")
    
    elif selected == "Verbeterpunten":
        st.markdown("""
                    ---\n\n
                    ## 8. Verbeterpunten\n\n
                    **Wat kan er volgens jouw beter aan de trainingen? En hoe?**\n\n
                    Dit kan er beter volgens de atleten:
                    """)
        for response in df_selection["Wat kan er volgens jouw beter aan de trainingen? En hoe?\n\nLaat hieronder jouw ideeën achter."]:
            if response == None:
                pass
            else:
                message = st.chat_message("human")
                message.write(response)