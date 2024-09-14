import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide')
df = pd.read_csv("C:/Users/hrutu/Downloads/startup_cleaned.csv")
# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Check for any NaT values in the 'date' column after conversion
if df['date'].isna().sum() > 0:
    st.write("Warning: Some date values could not be converted and will be ignored.")
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments of the investors
    last_5df=df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)

    #biggest investments
    col1 ,col2=st.columns(2)

    with col1:
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest Investments')
        st.dataframe(big_series.head())
    with col2:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False)
        top5_big_series = big_series.head()


        st.subheader('Biggest Investments graph')
        fig, ax = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax.bar(top5_big_series.index, top5_big_series.values)
        ax.set_xlabel('Startup')
        ax.set_ylabel('Total Investment Amount')
        ax.set_title('Biggest Investments by Startup')
        st.pyplot(fig)
    col3,col4=st.columns(2)
    with col3:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head(5)
        st.subheader('Sectorswise Investment Table')
        st.dataframe(vertical_series)

    with col4:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head(5)
        st.subheader('Sectorswise Investment')
        fig1, ax1 = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax1.pie(vertical_series,labels=vertical_series.index)
        st.pyplot(fig1)

    col4,col5=st.columns(2)
    with col4:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head(5)
        st.subheader('Stagewise Investment Graph')
        fig2, ax2 = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax2.bar(stage_series.index, stage_series.values)
        ax2.set_xlabel('Stage')
        ax2.set_ylabel('Total Investment Amount')
        ax2.set_title('Round by Investment')
        st.pyplot(fig2)
    with col5:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head(5)
        st.subheader('Citywise Investment Graph')
        fig3, ax3 = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax3.bar(city_series.index, city_series.values)
        ax3.set_xlabel('City')
        ax3.set_ylabel('Total Investment Amount')
        ax3.set_title('City by Investment')
        st.pyplot(fig3)

    #Extract year from date column
    # Extract year from the 'date' column
    df['year'] = df['date'].dt.year

    # Group by year and sum the amounts
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('Year-wise Investment Graph')
    fig4, ax4 = plt.subplots()
    ax4.bar(year_series.index, year_series.values)
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Total Investment Amount')
    ax4.set_title(f'Year-wise Investment for {investor}')
    st.pyplot(fig4)

def load_overall_analysis():
    st.title('Overall Analysis')
    #total invested amounr
    total=round(df['amount'].sum())
    max = round(df['amount'].max())
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    total_funded_startup=df['startup'].nunique()
    col6,col7,col8,col9=st.columns(4)
    with col6:
        st.metric('Total', str(total) + ' Cr')
    with col7:
        st.metric('Max Funding', str(max) + ' Cr')
    with col8:
        st.metric('Avg Funding', str(round(avg_funding)) + ' Cr')
    with col9:
        st.metric('Funded Startups', str(round(total_funded_startup)))

    col10,col11=st.columns(2)
    with col10:
        st.header('Month-Month Graph')
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index().head()
        temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        fig5, ax5 = plt.subplots()
        ax5.plot(temp_df['x-axis'], temp_df['amount'], marker='o')
        ax5.set_xlabel('Year')
        ax5.set_ylabel('Total Investment Amount')
        ax5.set_title('Month-Month Analysis')
        st.pyplot(fig5)
    with col11:
        df_overall_round = df.groupby(['round'])['amount'].sum().head(5)
        st.subheader('Fundingwise Investment')
        fig6, ax6 = plt.subplots()
        ax6.plot(df_overall_round.index, df_overall_round.values, marker='o')
        ax6.set_xlabel('Funding')
        ax6.set_ylabel('Total Investment Amount')
        ax6.set_title('Funding by Investment')
        st.pyplot(fig6)
    col12,col13=st.columns(2)
    with col12:
        df_city = df.groupby(['city'])['amount'].sum().sort_values(ascending=False).head()

        st.subheader('Overall Citywise Investment')
        fig7, ax7 = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax7.pie(df_city, labels=df_city.index)
        st.pyplot(fig7)
    col14,col15=st.columns(2)
    with col14:
        df_top = df.groupby(['startup'])['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Top Startups')
        fig8, ax8 = plt.subplots()
        ax8.plot(df_top.index, df_top.values, marker='o')
        ax8.set_xlabel('Startups')
        ax8.set_ylabel('Total Investment Amount')
        ax8.set_title('Startup by Investment')
        st.pyplot(fig8)

def load_startup_analysis(startup):
    st.title('StartUp Analysis')
    st.title(startup)
    vertical = df[df['startup'].str.contains(startup)]['vertical']
    st.dataframe(vertical)
    city= df[df['startup'].str.contains(startup)]['city']
    st.dataframe(city)
    col16,col17=st.columns(2)
    with col16:
        st.subheader('Investorwise Investment')
        investor_table = df[df['startup'].str.contains(startup)].groupby('investors')['amount'].sum()
        st.dataframe(investor_table)

    with col17:
        investor_table = df[df['startup'].str.contains(startup)].groupby('investors')['amount'].sum()
        st.subheader('Investorwise Investment')
        fig9, ax9 = plt.subplots()  # Use plt.subplots() to create the figure and axes
        ax9.pie(investor_table, labels=investor_table.index)
        st.pyplot(fig9)


    round = df[df['startup'].str.contains(startup)].groupby('round')['amount'].sum()
    st.dataframe(round)
    df_date= df[df['startup'].str.contains(startup)].groupby('investors')['date']
    st.dataframe(df_date)




st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':

    btn0=st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()

elif option=='Startup':
    selected_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_analysis(selected_startup)

else:
    selected_investor=st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    st.title('Investor Analysis')
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)

