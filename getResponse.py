from read_spreadsheet import df_sheet
import sys
from work_allocation import give_work_link_name
import configs
from google_trans import translate_text
import html
import mongo_funcs
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
    
    if lang_response == "ro":
    
        r_default= """
        <b>(RO)</b>Ofera 5 minute pentru a lupta cu dezinformarea.
        Ai 2 opțiuni:
        *scrie <b>"ok"</b> :primește un profil de raportat
        *trimite un link de facebook suspicios (profil, grup, postare sau pagină), 
        impreună cu detalii precum nume& prenume al profilului și o scurtă descriere.
        (Mesajele sunt traduse în limba de comunicare aleasă de dvs pe telegram : ro)""".replace("  ","")
    
    elif lang_response == "ru":

        r_default = """
                <b>(RU)</b>потрать 5 минут на репорт тролля/
                У вас есть 2 варианта:
                *напишите <b> "ok" </b>: получите профиль для отчета
                *отправьте подозрительную ссылку на facebook 
                (профиль, группу, пост) вместе с такими данными, 
                как имя и фамилия профиля, а также кратким описанием
                (Сообщения переводятся на выбранный вами язык телеграммой: русский)""".replace("  ","")
    
    elif lang_response == "en":
        r_default ="""
            <b>(EN)</b>Give 5 minutes to fight fake news and manipulations on facebook.
            You got 2 options:
            *write <b>"ok"</b> : get a facebook link to report
            *send a facebook link that raises suspicions, together with the name of the profile and short description
            (Messages are translated into the language of your choice by telegram: en)
            """.replace("  ","")
    else: 
        r_default_en =f"""
        <b>(EN)</b>Give 5 minutes to fight fake news and manipulations on facebook.
        You got 2 options:
        *write <b>"ok"</b> : get a facebook link to report
        *send a facebook link that raises suspicions, together with the name of the profile and short description
        (Messages are translated into the language of your choice by telegram: {lang_response})
        """.replace("  ","")
        replyDB_translated = translate_text(target_language=lang_response, text= r_default_en)
        r_default = html.unescape(replyDB_translated["translatedText"])

    
    r_final = r_default
    try:
        Link_Name_List= give_work_link_name(Telegram_ID)
        
        if len(Link_Name_List)==0:   
            print("1. Link 0")     
            replyDB_EN= "Thank you, but there are no more available links. Try again later."
            replyDB_translated = translate_text(target_language=lang_response, text= replyDB_EN)
            replyDB_translated_text= html.unescape(replyDB_translated["translatedText"])
            
            r_final = replyDB_translated_text
        else:
            shx_link = Link_Name_List[0]
            shx_name= Link_Name_List[1]
            shx_comments = Link_Name_List[2]
            if len(shx_comments)<4:
                shx_comments= "Promotes fake news"

            if (user_input.lower() == "ok") or (user_input.lower() =="ок"):
                if not mongo_funcs.Limit_ok(Telegram_ID, configs.Limit_ok_Days, configs.Limit_ok_Nr):
                    try:
                        comments_translated = translate_text(target_language=lang_response, text= shx_comments)
                        comments_translated_text= html.unescape(comments_translated["translatedText"])
                        r_final = f"<b>{shx_name}</b>\n-{comments_translated_text}-\n{shx_link}\n"
                    except:
                        r_final = f"{shx_link}\n"
                    print("2. final ok")
                else:
                    rejected_str = f"Vă mulțumim pentru ajutor. Vă rugăm să încercați mai târziu pentru alte linkuri. În ultimele {configs.Limit_ok_Days} zile ați primit {configs.Limit_ok_Nr} linkuri de raportat"
                    rejected = translate_text(target_language=lang_response, text= rejected_str)
                    rejected_text= html.unescape(rejected["translatedText"])
                    r_final = rejected_text
                    print("3. Over limit")
            
            elif "facebook.com" in user_input.lower():
                replyDB_EN= "Thank you, the provided link will be added to the Database. Please provide more information about the link shared."
                replyDB_translated = translate_text(target_language=lang_response, text= replyDB_EN)
                replyDB_translated_text= html.unescape(replyDB_translated["translatedText"])
                
                r_final = replyDB_translated_text
                print("4. FB")
            
            elif "photo" in user_input.lower():
                replyDB_EN= "Thank you, the provided photo will be added to the Database. Please provide more information about the photo shared."
                replyDB_translated = translate_text(target_language=lang_response, text= replyDB_EN)
                replyDB_translated_text= html.unescape(replyDB_translated["translatedText"])

                r_final = replyDB_translated_text
                print("5. PHOTO")
            elif user_input.lower() == "notvalid":
                replyDB_EN= "Please write <ok> to receive a link to report or provide us with a facebook link"
                replyDB_translated = translate_text(target_language=lang_response, text= replyDB_EN)
                replyDB_translated_text= html.unescape(comments_translated["translatedText"])
                
                r_final = replyDB_translated_text
                print("6. Final elif")
            else:
                r_final = r_default
                print("7. Final else")
    except Exception as e:
        print(e)

    return r_final

if __name__ == "__main__":
    print("Executing the main")
else: 
    print(f"Imported {sys.argv[0]}")