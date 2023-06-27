# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

#page config
icon = Image.open("ICN.png")
st.sidebar.image("img.png")


#connecting mysql
mydb = sql.connect(host="localhost",
                   user="root",
                   password="root",
                   database= "phonepe"
                  )
mycursor = mydb.cursor(buffered=True)

# creating option menu in side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
#menu Home
if selected=="Home":
    col1,col2=st.columns([2,3],gap="small")
    with col1:
         st.image("img.png")
         st.markdown("###### :white[PhonePe is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by sameer Nigam], Rahul Chari and Burzin Engineer. The PhonePe app, basex on the Unified Payments Interface(UPI), went live in August 2016.It is owned by Flipkart, a subsidiary of Walmart")
         st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://www.youtube.com/watch?v=aXnNA4mv1dU")

        st.write("")
    st.write("")
    st.write("")

    col1,col2=st.columns([4,1],gap="small")
    with col1:
        st.image("Home1.png")
    with col2:
         st.write(" ")
         st.write(" ")
         st.markdown("### :white[View Statements and manage Financial Consents]")
         
    st.write("")
    st.write("")
    st.write("")

    col1,col2=st.columns([1,4],gap="small")
    with col1:
         st.write(" ")
         st.write(" ")
         st.markdown("## :white[Beat of Progress]")
       
    with col2:
        st.image("Home2.png")

    
    st.write("")
    st.write("")
    st.write("")
        
    col1,col2=st.columns([4,1],gap="small")
    with col1:
        st.image("Home3.png")
    with col2:
         st.write(" ")
         st.write(" ")
         st.markdown("### :violet[Recharge, Pay Bills & Send money safely from home]")

#menu Top charts

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
#Top charts Transactions

    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select States, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from agg_trans where Transaction_Year = {Year} and Quarters = {Quarter} group by States order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"select District , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total from map_trans where Transaction_Year = {Year} and Quarters = {Quarter} group by District order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)


# top users

    if Type == "Users":
            col1,col2 = st.columns([2,3],gap="small")

            with col1:
                st.markdown("### :violet[Brands]")
                if Year == 2022 and Quarter in [2,3,4]:
                    st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
                else:
                    mycursor.execute(f"select Brand, sum(Count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from agg_user where Transaction_Year = {Year} and Quarters = {Quarter} group by Brand order by Total_Count desc limit 10")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                    fig = px.bar(df,
                                title='Top 10',
                                x="Total_Users",
                                y="Brand",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig,use_container_width=True) 

            with col2:
                st.markdown("### :violet[District]")
                mycursor.execute(f"select District, sum(RegisteredUsers) as Total_Users, sum(AppOens) as Total_Appopens from map_user where Transaction_Year = {Year} and Quarter = {Quarter} group by District order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                df.Total_Users = df.Total_Users.astype(float)
                fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

            col3,col4 = st.columns([2,3],gap="small")
              
            with col3:
                st.markdown("### :violet[Pincode]")
                mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where Transaction_Year = {Year} and Quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col4:
                st.markdown("### :violet[State]")
                mycursor.execute(f"select States, sum(RegisteredUsers) as Total_Users, sum(AppOens) as Total_Appopens from map_user where Transaction_Year = {Year} and Quarter = {Quarter} group by States order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)


# Explore Dta 
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
   

# transaction

    if Type == "Transactions":
        
    
    # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        
        st.markdown("## :red[Overall State Data - Transactions Amount]")
        mycursor.execute(f"select States, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_trans where Transaction_Year = {Year} and Quarters = {Quarter} group by States order by States")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('Statenames.csv')
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/Sandhiya-Sadhasivam/36658c549b5db8c2561abc926f9c66f0/raw/3a4996d3566bebbe56d2b4436a858ab4befb1800/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_amount',
                    
                    color_continuous_scale="sunset")

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

        
        st.markdown("## :red[Overall State Data - Transactions Count]")
        mycursor.execute(f"select States, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_trans where Transaction_Year = {Year} and Quarters = {Quarter} group by States order by States")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Transactions = df1.Total_Transactions.astype(int)
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='sunset')
            
        

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :red[Top Payment Type]")
        mycursor.execute(f"select Transaction_Type, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from agg_trans where Transaction_Year= {Year} and Quarters = {Quarter} group by Transaction_Type order by Transaction_Type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_Type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_Type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
            

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select States, District,Transaction_Year,Quarters, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_trans where Transaction_Year = {Year} and Quarters = {Quarter} and States= '{selected_state}' group by States, District,Transaction_Year,Quarters order by States,District")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['States','District','Transaction_Year','Quarters',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :red[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select States, sum(RegisteredUsers) as Total_Users, sum(AppOens) as Total_Appopens from map_user where Transaction_Year = {Year} and Quarter = {Quarter} group by States order by States")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/Sandhiya-Sadhasivam/36658c549b5db8c2561abc926f9c66f0/raw/3a4996d3566bebbe56d2b4436a858ab4befb1800/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Appopens',
                    color_continuous_scale='sunset')
        

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select States,Transaction_Year,Quarter,District,sum(RegisteredUsers) as Total_Users, sum(AppOens) as Total_Appopens from map_user where Transaction_Year = {Year} and Quarter = {Quarter} and States = '{selected_state}' group by States, District,Transaction_Year,Quarter order by States,District")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['States','Transaction_Year', 'Quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

#about

if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :red[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.jpg")

    st.markdown("### :red[About PhonePe:] ")
    st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        


        

    
   
 
        
    

        


