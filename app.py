import streamlit as st
import pandas as pd


#===============================
#データ読み込み・設定
#===============================


st.title("プロ野球選手 成績分析ツール")
st.write("2025年度セ・リーグの主要選手の成績を、",
         "条件指定・ランキング・選手比較によって分析できます。")
st.divider()


df = pd.read_csv("2025.hanshin.csv", encoding="cp932")
all_players = df.copy()
column_names = {"player":"選手名","team":"チーム",
                "avg":"打率","hr":"本塁打","rbi":"打点",
                "ops":"OPS"}



#===============================
# データの絞り込み・並び替え
#===============================

st.subheader("成績データの絞り込み・並び替え")

teams = ["すべて"]  + list(df["team"].unique())

selected_team = st.selectbox(
    "チームを選択してください",
    teams
)

if selected_team != "すべて":
    df = df[df["team"] == selected_team]

selected_stat = st.selectbox(
    "並べ替えの基準にする成績項目を選択してください",
    ["avg","hr","rbi","ops"],
    format_func=lambda x: column_names[x]
)
df = df.sort_values(selected_stat,ascending = False)

st.dataframe(df.rename(columns=column_names))



#===============================
#2選手の成績比較
#===============================
st.subheader("2選手の成績比較")

col1,col2 = st.columns(2)

with col1:
    selected_A = st.selectbox(
        "選手A",
        list(df["player"])
        )

with col2:
    selected_B = st.selectbox(
        "選手B",
        [player for player in df["player"] if player != selected_A]
        )

player_A = df[df["player"] == selected_A] 
player_B = df[df["player"] == selected_B]
player_A = player_A[["avg", "hr", "rbi", "ops"]]
player_B = player_B[["avg", "hr", "rbi", "ops"]]

player_A = player_A.reset_index(drop=True)
player_B = player_B.reset_index(drop=True)
player_A = player_A.T
player_B = player_B.T

player_A.columns = [selected_A]
player_B.columns = [selected_B]


df_compare = pd.concat([player_A,player_B],axis=1)
st.dataframe(df_compare.rename(index=column_names))



#===============================
#成績の可視化
#===============================
compare_A = player_A[selected_A][selected_stat]
compare_B = player_B[selected_B][selected_stat]

df_graph = pd.DataFrame({
    "選手名":[selected_A,selected_B],
    "成績":[compare_A,compare_B]
})

st.write(f"{column_names[selected_stat]}の比較")
st.bar_chart(df_graph,x = "選手名", y = "成績")



#===============================
#成績ランキング
#===============================
st.subheader("成績ランキング")


df_rank = all_players.copy()
rank_stat = st.selectbox("ランキングとして表示する成績を選んでください",
                         ["avg","hr","rbi","ops"],
                         format_func=lambda x:column_names[x])
df_rank["順位"] = df_rank[rank_stat].rank(
    ascending=False,method="min")
df_rank = df_rank.sort_values("順位",ascending=True)
df_rank_display = df_rank[["順位","player","team",rank_stat]]
df_rank_display = df_rank_display.rename(columns=column_names)


st.dataframe(df_rank_display)



#===============================
#全データを表示
#===============================
st.subheader("全主要選手一覧")
st.dataframe(all_players.rename(columns=column_names))
