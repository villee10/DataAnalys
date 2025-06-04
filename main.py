import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("diamonds.csv")
st.sidebar.header(" Filtrera diamanter")




# Sidebar
cut = st.sidebar.multiselect(" Välj cut", options=df["cut"].unique(), default=df["cut"].unique())
color = st.sidebar.multiselect(" Välj color", options=df["color"].unique(), default=df["color"].unique())
clarity = st.sidebar.multiselect(" Välj clarity", options=df["clarity"].unique(), default=df["clarity"].unique())

# Pris
price_min, price_max = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider(" Prisintervall", min_value=price_min, max_value=price_max,
                                value=(price_min, price_max))



# Filtrering
filtered_df = df[
    (df["cut"].isin(cut)) &
    (df["color"].isin(color)) &
    (df["clarity"].isin(clarity)) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]



# huvudsidan
st.title("Analys av diamanter")
st.markdown("""
Guldfynd undersöker möjligheten att börja sälja diamanter. Denna app visar en analys av ett diamant-dataset.
Använd filtren i sidopanelen för att undersöka olika attribut. 
""")





col1, col2, col3 = st.columns(3)
col1.metric(" Genomsnittspris", f"${filtered_df['price'].mean():,.0f}")
col2.metric(" Max carat", f"{filtered_df['carat'].max():.2f}")
col3.metric(" Antal diamanter", len(filtered_df))



st.subheader(" Filtrerad datatabell")
st.dataframe(filtered_df)

# diagram1
st.subheader(" Pris i förhållande till vikt (carat)")
st.write("Vi ser ett starkt samband: ju större carat, desto högre pris – särskilt efter 1.0 carat.")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered_df, x='carat', y='price', hue='cut', ax=ax1)
ax1.set_title("Pris vs Carat")
st.pyplot(fig1)

# diagram2
st.subheader(" Prisdistribution")
st.write("De flesta diamanter kostar under 5 000 USD, vilket kan påverka sortimentsbeslut.")
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df['price'], bins=50, kde=True, ax=ax2)
ax2.set_title("Prisdistribution")
st.pyplot(fig2)

# diagram3
st.subheader(" Medelpris per klarhet (clarity)")
st.write("Renare diamanter (t.ex. IF, VVS1) tenderar att ha högre genomsnittligt pris.")
mean_price = filtered_df.groupby("clarity")["price"].mean().sort_values()
fig3, ax3 = plt.subplots()
mean_price.plot(kind='barh', ax=ax3)
ax3.set_xlabel("Genomsnittligt pris (USD)")
ax3.set_title("Pris per clarity")
st.pyplot(fig3)

# summering
st.markdown("##  Executive Summary")
st.markdown(""" - **Carat** har störst påverkan på priset särskilt runt 1.0 carat.
- **Cut och clarity** påverkar pris, men i mindre grad.
- **Rekommendation:** Guldfynd bör fokusera på diamanter i området 0.9–1.1 carat, med bra cut och mellan hög clarity (VS1/VS2) för bästa värde.
""")


