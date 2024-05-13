import random
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from io import StringIO
from config import parsers
from utils import get_response, get_stream_response, save_to_doc, save_to_csv, get_files
import os

temperature = 0.7
top_k = 3
top_p = 0.5
n_beams = 2

args = parsers()

def gen_question(gen_type, question_type, question_input):
    return get_response(args.model_path[gen_type][question_type], question_input, args.system_prompt[gen_type][question_type], temperature, top_k, top_p)

def gen_stream_question(gen_type, question_type, question_input):
    for response in get_stream_response(args.model_path[gen_type][question_type], question_input, args.system_prompt[gen_type][question_type], temperature, top_k, top_p):
        yield response

def introduction_page():
    st.title("👨‍💻 C语言出题系统")
    with st.expander('**Welcome to 👨‍💻 C语言出题系统!**'):
        st.markdown('在编程教育和自我提升的过程中，高质量的练习题是不可或缺的。\n'
                '为了满足这一需求，我们开发了一个基于大模型微调的C语言试题自动生成系统，'
                '旨在通过先进的人工智能技术，提供定制化的C语言练习题，'
                '以帮助学习者和教师更高效地进行学习和教学。')

    with st.expander('**关于试卷一键生成**'):
        st.markdown('我们的C语言试题自动生成系统提供自动化试卷生成功能，允许用户上传文本形式的参考材料，'
                    '并根据用户设定的题型和数量，智能编排出一整张完整的试卷。这一功能特别适合需要快速准备教学材料或自我测试的学习者。'
                    '系统将确保试卷覆盖指定的题型及知识点，无论是教师备课还是学生自学，都能通过简单几步操作，'
                    '获得一份结构合理、内容丰富的试卷，极大提升了教学和学习的效率。')

    with st.expander('**关于出题工具包**'):
        st.markdown('本系统具备强大的题型生成与转换功能，能够根据用户指定的参考材料，智能生成四种主要的C语言题型：'
                '选择题、填空题、算法题和实际应用题。每种题型都旨在提升不同层面的编程技能，如逻辑推理、语法掌握、算法设计和解决实际问题的能力。'
                '此外，系统还支持题型之间的相互转换，例如，将选择题转换为填空题，或将算法题调整为实际应用题，以适应不同的教学策略和学习需求。'
                '这一创新功能不仅丰富了教学资源，也为个性化学习提供了可能，确保每位学习者都能在适合自己的方式中取得进步。')

    with st.expander('**关于对话交互**'):
        st.markdown('本系统引入了创新的对话式出题功能，用户可以直接与大模型进行交流，以自然语言的形式描述所需题型和难度。'
                    '系统将理解用户的需求，并生成相应的C语言试题。这种交互方式不仅提高了出题的灵活性，也使得试题生成过程更加直观和人性化。'
                    '通过对话，用户可以轻松定制试题内容，包括特定知识点的覆盖、题目难度的调整以及题型的多样化选择。'
                    '这种智能对话机制，将传统的试题生成转变为一种互动体验，极大地提升了用户的参与感和满意度。')

def paper_gen_page():
    st.title("📜 试卷一键生成")
    question_num = {}
    with st.expander('**自定义试卷组成**'):
        question_num['选择题'] = st.slider('📄选择题数量', 0, 10, 2)
        question_num['填空题'] = st.slider('📄填空题数量', 0, 10, 2)
        question_num['算法题'] = st.slider('📄算法题数量', 0, 10, 2)
        question_num['实际应用题'] = st.slider('📄实际应用题数量', 0, 10, 2)
                
    st.subheader('📑 知识点选择')
    
    chapter = {
        '第一章': '第1章 基本概念',
        '第二章': '第2章 运算符与表达式',
        '第三章': '第3章 控制流',
        '第四章': '第4章 函数与程序结构',
        '第五章': '第5章 指针与数组',
        '第六章': '第6章 结构',
        '第七章': '第7章 输入与输出',
        '第八章': '第8章UNIX系统接口'
    }
    add_point = []
    point_files_path = get_files(args.papers_path, '.xlsx')
    for file_path in point_files_path:
        papers_df = pd.read_excel(file_path, sheet_name=None)
        for sheet_name in papers_df:
            if sheet_name.find('试卷') != -1:
                add_point.extend(list(set(papers_df[sheet_name].iloc[:, -1].tolist())))
    knowledge_point = list(chapter.values())
    knowledge_point.extend(list(set(add_point)))
    options = st.multiselect(
        '请选择知识点，留空表示选取所有的知识点',
        knowledge_point,
        []
    )
    st.subheader('📎 RAG 个性化出题')

    uploaded_file_from_contents = st.file_uploader("上传参考文本（若不上传则根据默认的参考文本生成）", accept_multiple_files=True, type='xlsx')
    uploaded_file_from_papers = st.file_uploader("上传试卷题目（若不上传则根据默认的试卷题目生成）", accept_multiple_files=True, type='xlsx')
    if 'is_generated' not in st.session_state:
        st.session_state.is_generated = False
        st.session_state.question_paper = {}
        st.session_state.string_paper = ''
    if st.button('开始生成试卷'):
        selected_point = set(knowledge_point if len(options) == 0 else options)
        selected_question = []

        contents_path = get_files(args.contents_path, '.xlsx') if len(uploaded_file_from_contents) == 0 else uploaded_file_from_contents
        papers_path = get_files(args.papers_path, '.xlsx') if len(uploaded_file_from_papers) == 0 else uploaded_file_from_papers
        
        for file_path in contents_path: # 获取所有C语言教材资料
            contents_df = pd.read_excel(file_path, sheet_name=None)
            for sheet_name in contents_df:
                if chapter.get(sheet_name) is not None and chapter[sheet_name] in selected_point: # 判断选择的知识点是否有这一章
                    content_list = contents_df[sheet_name].iloc[:, 0].tolist()
                    for value in content_list:
                        selected_question.append([value, '基于C语言文本内容'])

        for file_path in papers_path: # 获取所有C语言试卷题目
            papers_df = pd.read_excel(file_path, sheet_name=None)
            for sheet_name in papers_df:
                if sheet_name.find('试卷') != -1:
                    for idx, row in papers_df[sheet_name].iterrows():
                        cur_question = row.tolist()
                        if cur_question[2] in selected_point: # 判断该知识点是否被选择
                            selected_question.append([cur_question[0], '基于已有的题目'])

        random.shuffle(selected_question)
        with st.status('生成试题中...'):
            gen_index = 0
            for question_type in question_num:
                st.write('生成' + question_type + '中...')
                st.session_state.question_paper[question_type] = []
                for i in range(question_num[question_type]):
                    st.write('正在生成第' + str(i + 1) + '道' + question_type + '中...')
                    gen_type = selected_question[gen_index][1]
                    content = args.prefix_prompt[gen_type][question_type] + selected_question[gen_index][0]
                    gen_index += 1
                    stream_question = ''
                    for data in gen_stream_question(gen_type, question_type, content):
                        stream_question = stream_question + data
                    st.session_state.question_paper[question_type].append(stream_question)

        st.session_state.string_paper = ''
        question_index = 1
        for question_type in question_num:
            st.session_state.string_paper = st.session_state.string_paper + '\n' + question_type + '：\n'
            for question in st.session_state.question_paper[question_type]:
                st.session_state.string_paper = st.session_state.string_paper + str(question_index) + '. ' + str(question) + '\n\n'
                question_index += 1
        st.session_state.is_generated = True

    if st.session_state.is_generated == True:
        st.divider()
        st.subheader('📰 生成试卷展示')

        st.dataframe(st.session_state.question_paper)

        save_to_doc(st.session_state.string_paper, args.save_doc_path)
        with open(args.save_doc_path, 'rb') as file:
            st.download_button('导出为word', data=file, file_name='C_paper.docx')

        save_to_csv(st.session_state.question_paper, args.save_csv_path)
        with open(args.save_csv_path, 'rb') as file:
            st.download_button('导出为csv', data=file, file_name='C_paper.csv')

def question_gen_page():
    st.title("📦 出题工具包")
    with st.expander('**功能选择**', expanded=True):
        choose_character = st.selectbox('选择你的出题方式：', ["基于C语言文本内容", "基于已有的题目"], index=0)
        st.divider()
        st.subheader(choose_character)
        selectbox_exp = {
            '基于C语言文本内容': '通过输入C语言相关的知识点、教材内容、参考资料等文本，根据该文本生成一道题目。',
            '基于已有的题目': '通过输入一道已有的C语言题目，将该题目的题型转换为目标题型。'
        }
        st.caption(selectbox_exp[choose_character])
        question_type = st.radio(
            " ",
            horizontal=True,
            options=["选择题", "填空题", "算法题", "实际应用题"],
        )

        parameters = {
            '选择题': '生成一道C语言选择题',
            '填空题': '生成一道C语言填空题',
            '算法题': '生成一道C语言算法题',
            '实际应用题': '生成一道C语言实际应用题'
        }

        question_input = st.text_area(question_type, "", placeholder='请输入内容！', help=parameters[question_type], height=200, key='question_input')
        if st.button(label="提交"):
            st.divider()
            st.write(':green[**查看结果**]')
            result_content = st.write_stream(gen_stream_question(choose_character, question_type, args.prefix_prompt[choose_character][question_type] + question_input))
            st.divider()
            st.download_button('下载结果文本', result_content, file_name='result.txt')

def chat_page():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好，我是一个C语言出题大模型，有什么需要帮忙的？"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("输入文本"):
        st.chat_message("user").write(prompt)
        response = st.chat_message('assistant').write_stream(get_stream_response(args.model_path['对话模型'], prompt, st.session_state.messages, temperature, top_k, top_p))
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})

# 设置网页标题
st.set_page_config(page_title="IDKE-CPLLM", page_icon="👨‍💻")

# 设置侧栏
with st.sidebar:
    selected = option_menu(
        "  👨‍💻 C语言大模型",
        ["使用介绍", "试卷一键生成", "出题工具包","对话交互"],
        icons=["bi bi-book", "bi bi-chat-left-dots", "bi bi-brightness-alt-high", "bi bi-robot"],
        menu_icon="bi bi-arrow-right",
        default_index=0,
    )
            
    st.subheader('模型设置')   
    choose_model = st.selectbox('💡Choose Model', ['Chat-GLM'], help = "🔒敬请期待")
    temperature = st.slider('💡Temperature', 0.0, 1.0, 0.2)
    top_k = st.slider('💡Top_k', 1, 10, 3)
    top_p = st.slider('💡Top_p', 0.0, 1.0, 0.5)
    n_beams = st.slider('💡N_beams', 1, 5, 2)
    st.button('保存设置')
    
if selected == "使用介绍":
    introduction_page()
elif selected == "试卷一键生成":
    paper_gen_page()
elif selected == "出题工具包":
    question_gen_page()
elif selected == "对话交互":
    chat_page()
