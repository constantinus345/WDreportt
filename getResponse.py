from read_spreadsheet import df_sheet
import sys
from work_allocation import give_work_link_name
import configs
from google_trans import translate_text

#Sheet_x1 = "Suspect or fake profiles"
#df_sheet_x1 = df_sheet(Sheet_x1)

#print(Sheet_x1)
#print(list(df_sheet_x1))

"""shx1_name= df_sheet_x1["Name of profile"][0]
shx1_link = df_sheet_x1["Link"][0]
shx1_status = df_sheet_x1["Status"][0]"""






"""    if ro.ok: r_final= <a href="url">link text</a>
    elif ru.ok 
    elif ”facebook.com” in reply: r_final = Multumesc&Spasiba pentru link
    else: r_final= r_default
    <a href="url">link text</a>"""

def getResponse(user_input, Telegram_ID, lang_response):
    
    r_default= """<b>(RO)</b>Ofera 5 minute pentru a lupta cu dezinformarea.
    Ai 2 opțiuni:
    *scrie <b>"ok"</b> :primește un profil de raportat
    *trimite un link de facebook suspicios (profil, grup, postare sau pagină), 
    impreună cu detalii precum nume& prenume al profilului și o scurtă descriere

    <b>(RU)</b>потрать 5 минут на репорт тролля/
     У вас есть 2 варианта:
     *напишите <b> "ok" </b>: получите профиль для отчета
     *отправьте подозрительную ссылку на facebook 
     (профиль, группу, пост) вместе с такими данными, 
     как имя и фамилия профиля, а также кратким описанием

    <b>(EN)</b>Give 5 minutes to fight fake news and manipulations on facebook.
    You got 2 options:
    *write <b>"ok"</b> : get a facebook link to report
    *send a facebook link that raises suspicions, together with the name of the profile and short description
    """.replace("  ","")
    
    r_final = r_default

    Link_Name_List= give_work_link_name(Telegram_ID = configs.Telegram_ID_C)

    shx_link = Link_Name_List[0]
    shx_name= Link_Name_List[1]
    shx_comments = Link_Name_List[2]

    if (user_input.lower() == "ok") or (user_input.lower() =="ок"):
        comments_translated = translate_text(target_language=lang_response, text= shx_comments)["translatedText"]
        r_final = f"{shx_link}\n{shx_name}\n{comments_translated}"
    elif "facebook.com" in user_input.lower():
        r_final ="Mulțumesc, linkul a fost recepționat\n\nСпасибо, ссылка была зарегистрирована"
    else:
        r_final = r_default

    return r_final

if __name__ == "__main__":
    print("Executing the main")
else: 
    print(f"Imported {sys.argv[0]}")