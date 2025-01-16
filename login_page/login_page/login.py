from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

def main():
  win-TK()
  app=Login.Window(win)
  win.mainloop()













class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x900+0+0")

        # Update the file path to the image if it's not in the same directory
        self.bg = ImageTk.PhotoImage(file="IIstock.jpg")
        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        frame=Frame(self.root,bg="turquoise4")
        frame.place(x=610,y=170,width=340,height=450)

        img1=Image.open("user3.jpg")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="turquoise4",borderwidth=0)
        lblimg1.place(x=730,y=175,width=100,height=100)

        get_str=Label(frame,text="Get Started",font=("times new roman ",20,"bold"),fg="white",bg="turquoise4")
        get_str.place(x=95,y=100)

        # ========labells=====
        username=lbl=Label(frame,text="Username",font=("times new roman ",15,"bold"),fg="white",bg="turquoise4")
        username.place(x=70,y=155)

        self.txtuser=Entry(frame,font=("times new roman ",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        password=lbl=Label(frame,text="Password",font=("times new roman ",15,"bold"),fg="white",bg="turquoise4")
        password.place(x=70,y=248)

        self.txtpass=Entry(frame,font=("times new roman ",15,"bold"))
        self.txtpass.place(x=40,y=275,width=270)

      #   ==========Icon Image=========
        img2=Image.open("user3.jpg")
        img2=img2.resize((25,25),Image.ANTIALIAS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg1=Label(image=self.photoimage2,bg="turquoise4",borderwidth=0)
        lblimg1.place(x=650,y=323,width=25,height=25)


        img3=Image.open("lock.png")
        img3=img3.resize((25,25),Image.ANTIALIAS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg1=Label(image=self.photoimage3,bg="turquoise4",borderwidth=0)
        lblimg1.place(x=650,y=419,width=25,height=25)
        
        # ========Login Buttons========
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman ",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="turquoise4",activeforeground="turquoise4")
        loginbtn.place(x=110,y=313,width=120,height=32)
        
        # =========Register button==========
        Regbtn=Button(frame,text="Register new User",command=self.register_window,font=("times new roman ",10,"bold"),borderwidth=0,fg="black",bg="turquoise4",activeforeground="white",activebackground="turquoise4")
        Regbtn.place(x=92,y=375,width=160)
        
        # =========Forget button button==========
        frgbtn=Button(frame,text="Forget Password",font=("times new roman ",10,"bold"),borderwidth=0,fg="black",bg="turquoise4",activeforeground="white",activebackground="turquoise4")
        frgbtn.place(x=110,y=350,width=120)




    def register_window(self):
      self.new_window=Toplevel(self.root)
      self.app=Register(self.new_window)











    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
          messagebox.showerror("Error",'Please fill the required fields')
        elif self.txtuser.get()=="chat" and self.txtpass.get()=="bot":
          messagebox.showerror("Succes",'Welcome to the chatbot')
        else:
          conn=mysqi=l.connector.connect(host="localhost",user="root",password="Test@123",database="mydata")
          my_cursor=conn.cursor()
          my_cursor.execute("select *from register where email=%s and password=%s",(self.var_email.get(),self.var_pass.get()))

          row=my_cursor.fetclone()
          if row!=None:

              messagebox.showerror('Error','Invalid username and password')

          # else:
          #     open_main=messagebox.askyesno("YesNo","only admin") 
          #     if open_main>0:
          #       self.new_window=Toplevel(self.new_window)
          #       self.app=








class Register:  
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")
# variables

        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()  # email id
        self.var_pass = StringVar()   #<PASSWORD>
        self.var_confpass=StringVar()    ##confirm password






#bg image
        self.bg=ImageTk.PhotoImage(file="")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

#left Image
        self.bg1=ImageTk.PhotoImage(file="")
        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100,width=470,height=550)

#main frame
        frame=Frame(self.root,bg="white")
        frame.place(x=520,y=100,width=800,height=550)


        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",25,"bold"),fg="darkgreen",bg="white")
        register_lbl.place(x=20,y=20)

#label and entry 
#row 1

        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry(frame, textvariable==self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=130,width=250)


        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame, textvariable==self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)


        # row 2

        contact=Label(frame,text="Contact No.",font=("times new roman",15,"bold"),bg="white",fg="black")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable==self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)



        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable==self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

# row 3


        # security_Q=Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white",fg="black")
        # security_Q.place(x=50,y=240)

        # self.txt_lname=ttk.Entry(frame,font=("times new roman",15))
        # self.txt_lname.place(x=370,y=130,width=250)

#Z row 4
        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable==self.var_pass,font=("times new roman",15))
        self.txt_pswd.place(x=50,y=340,width=250)


        confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        confirm_pswd.place(x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable==self.var_confpass,font=("times new roman",15))
        self.txt_confirm_pswd.place(x=370,y=340,width=250)


#checkbutton
        self.var_check=IntVar()
        self.checkbtn=Checkbutton(frame, textvariable==self.var_check,text="I Agree The Term & Conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        self.checkbtn.place(x=50,Y=380)

        #BUTTON

        img=Image.open("")
        img=img.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img)
        b1=Button(frame,image=self.photoimage, command=self.register_data , borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white")
        b1.place(x=10,y=420,width=200)



        img1=Image.open("")
        img1=img1.resize((200,50),Image.ANTIALIAS)
        self.photoimage=ImageTk.PhotoImage(img1)
        b1=Button(frame,image=self.photoimage,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white")
        b1.place(x=330,y=420,width=200)



# function Declaration
    def register_data(self):
        if self.var_fname.get()==""or self.var_email.get()=="Select":
            messagebox.showerror("Error","All Field are required")
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","password and Confirm password does not match.")
        elif self.var_check.get()==0:
            messagebox.showerror("error","Please agree our terms and conditions")
        else :
            conn =mysql.connector.connect(host="localhost",user="root",password="Test@123",database="mydata")
            my_cursor=com.cursor()
            query=("select*from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User alredy exist,plaese try another email")
            else:
                my_cursor.execute("insert into register value(%s,%s,%s,%s,%s,%s,%s)",(self.var_fname.get(),self.var_lname.get(),self.var_contact.get(),self.var_email.get(),self.var_pass.get(),self.var_confpass.get()))

            conn.commit()
            conn.close()
            messagebox.showinfo("success","Register Successfully")






if __name__ == "__main__": 
    main()