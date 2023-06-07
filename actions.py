from typing import Any, Text, Dict, List
import openai
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

openai.api_key = "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"

def chatgpt_clone(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt,
    temperature=1,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0.6,
    presence_penalty=0.6,
    )
    print(response.choices[0].text)
    return response.choices[0].text
class ActionGreet(Action):
    def name(self):
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        textex=tracker.latest_message['text']
        text = "Đây là một cuộc trò chuyện giữa người và chatbot giáo dục. Hãy trả lời câu "+ str(textex) +", đồng thời hỏi tên người đó và không nói tiếp bất cứ gì hết."
        answer=chatgpt_clone(text)
        dispatcher.utter_message(template="utter_greet",text=answer)
        return []
    
class ActionHelp(Action):
    def name(self):
        return "action_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        textex=tracker.latest_message['text']
        text = "Đây là một cuộc trò chuyện giữa người và AI chatbot tư vấn giáo dục với chức năng hỗ trợ về giáo dục. Hãy trả lời câu " + textex + " một cách ngắn gọn"
        answer=chatgpt_clone(text)
        dispatcher.utter_message(template="utter_help",text=answer)
        return []
    

class ActionDiemchuan(Action):
    def name(self):
        return "action_diem_chuan_va_truong"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # text=tracker.latest_message['text']
        university = tracker.get_slot("university")
        majors = tracker.get_slot("majors")
        import pandas as pd
        a=0
        df = pd.read_csv('database/data.csv')
        nganh = df['ngành']
        truong=df['trường']
        diem=df['điểm']
        for i, col in enumerate(nganh):
            if majors in col:
                print(diem[i])       
                a=diem[i]
        text = f"Ngành {majors} {university} có điểm chuẩn là {a}"
        dispatcher.utter_message(template="utter_diem_chuan_va_truong",text=text)
        return []

class ActionTohopMon(Action):
    def name(self):
        return "action_to_hop_mon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import pandas as pd
        block = tracker.get_slot("block")
        df = pd.read_csv('database/block.csv')
        khoi = df['KHỐI']
        Mon1 = df['Môn 1']
        Mon2 = df['Môn 2']
        Mon3 = df['Môn 3']
        for i, col in enumerate(khoi):
                if block in col:
                    a=Mon1[i]
                    b=Mon2[i] 
                    c=Mon3[i]      

        text = f"Khối {block} gồm những môn {a}, {b}, {c} "
        print(text)
        dispatcher.utter_message(template="utter_to_hop_mon",text=text)
        return []
    
class ActionNganhA(Action):
    def name(self):
        return "action_nganhA_dao_tao"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nganh = tracker.get_slot("majors")
        text=""
        import openpyxl
        workbook = openpyxl.load_workbook('database/data1.xlsx')
        sheet = workbook['data1']
        for row in sheet.iter_rows(min_row=2, min_col=1, max_col=2):

            name = row[0].value
            content = row[1].value
            
            if nganh in name:
                
                print(f"{name}\n{content}\n")
                text+= content
        dispatcher.utter_message(template="utter_nganhA_dao_tao",text=text)
        return []
    
class ActionDefault(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text=tracker.latest_message['text']
        answer=chatgpt_clone(text)
        dispatcher.utter_message(template="utter_default",text=answer)
        return []
    
class ActionReview(Action):
    def name(self):
        return "action_review_truong"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university = tracker.get_slot("university")
        text=f"""
        Trường {university} là ngôi trường có chất lượng đào tạo đạt chuẩn Quốc tế của hệ thống Đại học ASEAN. 
        Đây là cái nôi ươm mầm cho nhân tài đất Việt. Trong những năm qua trường đã gặt hái nhiều thành tích nhiều thành tích, thu hút sinh viên cả nước nộp hồ sơ vào. 
        Nếu bạn đang quan tâm về trường, hãy vào trang ctu.edu.vn để tìm hiểu nhé!"""
        dispatcher.utter_message(template="utter_review_truong",text=text)
        return []
    
class ActionMajors(Action):
    def name(self):
        return "action_info_majors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        university = tracker.get_slot("university")
        majors = tracker.get_slot("majors")
        text=f"Cảm ơn bạn đã quan tâm ngành {majors} của trường {university}. Ngành {majors} sẽ đào tạo bạn trở thành kĩ sư, trở thành một nhân tài của đất nước. Nếu bạn có đam mê thì trường {university} là một nơi tốt đồng hành, chắp cánh ước mơ cho bạn"
        dispatcher.utter_message(template="utter_info_majors",text=text)
        return []
    