import tkinter as tk 
from tkinter import ttk
from tkinter import Menu 
from preprocess import get_df
from tkinter import messagebox as mBox


win = tk.Tk()
win.title("Student Performance Prediction")
win.geometry("870x420")

menuBar = Menu(win)
win.config(menu=menuBar)

def _quit(): # 7
    win.quit()
    win.destroy()
    exit()


tabControl = ttk.Notebook(win) # Create Tab Control
predictoinTab = ttk.Frame(tabControl) # Create a tab
tabControl.add(predictoinTab, text='Prediction Menu') # Add the tab
tabControl.pack(expand=1, fill="both") # Pack to make visible

stats = ttk.Frame(tabControl) # Add a second tab
tabControl.add(stats, text='Statistics')


fileMenu = Menu(menuBar)
fileMenu.add_command(label="Add Student")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)
menuBar.add_cascade(label="File", menu=fileMenu)


helpMenu = Menu(menuBar, tearoff=0) # 6
helpMenu.add_command(label="App Info")
menuBar.add_cascade(label="Help", menu=helpMenu)



info = ttk.LabelFrame(predictoinTab, text='Student Info')
info.grid(column=0, row=0, sticky='W')

labelRow1 = ttk.LabelFrame(info, text='')
labelRow1.grid(column=0, row=0, sticky='W')

labelFrameSexAge = ttk.LabelFrame(labelRow1, text='Basic Info')
labelFrameSexAge.grid(column=0, row=0, sticky='W')

labelFrameSemI = ttk.LabelFrame(labelRow1, text='Semester I Scores')
labelFrameSemI.grid(column=1, row=0, sticky='W')

labelFrameSemII = ttk.LabelFrame(labelRow1, text='Semester II Scores')
labelFrameSemII.grid(column=2, row=0, sticky='W')

labelRow2 = ttk.LabelFrame(info, text='')
labelRow2.grid(column=0, row=1, sticky='W')


labelFrameQ = ttk.LabelFrame(labelRow2, text='Closed Loop Questions')
labelFrameQ.grid(column=0, row=0, sticky='W')

labelPrediction = ttk.LabelFrame(labelRow2, text='Prediction Results')
labelPrediction.grid(column=1, row=0, sticky='W')


ttk.Label(labelFrameSexAge, text = "Age: ").grid(column=0, row=0, sticky='W')
age = tk.StringVar()
ageText = ttk.Entry(labelFrameSexAge, width=12, textvariable=age)
ageText.grid(column=1, row=0)

ttk.Label(labelFrameSexAge, text = "Sex: ").grid(column=0, row=1, sticky='W')
sex = tk.StringVar()
sexChosen = ttk.Combobox(labelFrameSexAge, width=10, textvariable=sex, state='readonly')
sexChosen['values'] = ['--Choose--', 'Male', 'Female']
sexChosen.grid(column=1, row=1)
sexChosen.current(0)


def pad_xy(frame, x = 6, y = 4):
    for child in frame.winfo_children():
        child.grid_configure(padx = x, pady = y)




def get_course_label(i):
    courses = ['English', 'Math', 'Physics', 'Chemistry', 'Biology']
    return courses[i%5]


courseVal = []
courseField = []
for i in range(10):
    courseVal.append(tk.StringVar())
for i in range(10):
    if i < 5:
        ttk.Label(labelFrameSemI, text=get_course_label(i)).grid(column= 0, row=i, sticky='W')
        courseField.append(ttk.Entry(labelFrameSemI, width=10, textvariable=courseVal[i]))
        courseField[i].grid(column=1, row=i, sticky='W')
    else:
        ttk.Label(labelFrameSemII, text=get_course_label(i)).grid(column= 2, row=i%5, sticky='W')
        courseField.append(ttk.Entry(labelFrameSemII, width=10, textvariable=courseVal[i]))
        courseField[i].grid(column=3, row=i%5, sticky='W')
        

Qs = [
    '1) How do you rate the quality of education in your school?',
    '2) Who are your legal guardians?',
    '3) What is the average income of your family?',
    '4) What is the maximum level of education of your parents?',
    '5) Do you get extra help, such as tutorial, at home?',
    '6) What is your Grade 10 matriculation result?',
    '7) What is your parents occupation?',
    '8) Do you think education is helpful for your future?'
]

ans = [
    ['-----Select-----', 'Satisfactory', 'Good', 'Very Good', 'Excellent'],
    ['-----Select-----', 'Mother and Father', 'Mother Only', 'Father Only', 'Siblings', 'Other Relatives', 'I Live Alone'],
    ['-----Select-----', 'Less Than 5000', '5000-10000', '10000-20000', 'More Than 20000'],
    ['-----Select-----', 'No Education', 'High SchoolDropout', 'High School', 'Diploma', 'Degree', 'Masters', 'PhD'],
    ['-----Select-----', 'Yes', 'No'],
    ['-----Select-----', '2-2.5', '2.5-3', '3-3.5', '3.5-4'],
    ['-----Select-----', 'Trading', 'Artisan', 'Civil Servant', 'Military'],
    ['-----Select-----', 'Yes', 'No']
]




answerChosen = []
Qs_val = []
for i in range(8):
    Qs_val.append(tk.StringVar())

for i in range(8):
    ttk.Label(labelFrameQ, text=Qs[i]).grid(column=0, row=i, sticky='W')
    answerChosen.append(ttk.Combobox(labelFrameQ, width=15, textvariable=Qs_val[i], state='readonly'))
    answerChosen[i]['values'] = ans[i]
    answerChosen[i].current(0)
    answerChosen[i].grid(column=1, row=i)



# Prediction View
ttk.Label(labelPrediction, text='Result').grid(column=1, row=0, sticky='W')
ttk.Label(labelPrediction, text='Probability').grid(column=2, row=0, sticky='W')
predictionLabels = []
probabLabels = []
for i in range(5):

    ttk.Label(labelPrediction, text=get_course_label(i)).grid(column=0, row=2+i, sticky='W')
    predictionLabels.append(ttk.Label(labelPrediction, text='  NaN'))
    predictionLabels[i].grid(column=1, row=2+i, sticky='W')
    probabLabels.append(ttk.Label(labelPrediction, text='  NaN'))
    probabLabels[i].grid(column=2, row=2+i, sticky='W')



def _predict():
    inp = []

    if sexChosen.get() == 'Choose':
        mBox.showerror('Error occured!', 'You did not choose sex of student!')
    else:
        inp.append(sexChosen.get()[0])

    if not ageText.get().isdigit():
        mBox.showerror('Error!', 'Please Enter a number')
    else:
        inp.append(int(ageText.get()))


    for i in range(10):
        if not courseField[i].get().isdigit():
            mBox.showerror('Error!', 'Please Enter a number')
        else:
            inp.append(courseField[i].get())

    for i in range(8):
        if answerChosen[i].get() == '-----Select-----':
            mBox.showerror('Error occured!', 'You did not choose an answer for the question, ' + Qs[i][3:])
        else:
            inp.append(answerChosen[i].get())



    prediction_res, probab_res = get_df.predict(inp)
    for i in range(5):
        if prediction_res[i] == 'Fail':
            predictionLabels[i].configure(foreground='red')
        else:
            predictionLabels[i].configure(foreground='black')
        predictionLabels[i].configure(text=prediction_res[i])
        probabLabels[i].configure(text="{0:.3f}".format(round(probab_res[i],2)))



action = ttk.Button(labelPrediction, text="Predict", command=_predict)
action.grid(column=0, row=7) 



pad_xy(labelFrameSemI, y=2)
pad_xy(labelFrameSemII, y=2)
pad_xy(labelRow2)
pad_xy(labelRow1)
pad_xy(labelFrameQ)
pad_xy(labelFrameSexAge)
pad_xy(labelPrediction)
pad_xy(info)



win.mainloop()