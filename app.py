
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="智慧美食與冰箱管理",
    page_icon="🥗",
    layout="wide"
)

# ---------- 基本設定 ----------
st.markdown("""
<style>
.stApp { background-color: #f7f8f2; }
h1, h2, h3 { color: #365c45; }
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🥗 智慧美食與冰箱管理")
st.caption("Smart Food & Fridge Manager｜減少剩食，吃得更健康")

# ---------- 範例料理資料 ----------
RECIPES = [
    {
        "name": "番茄炒蛋",
        "ingredients": ["番茄", "雞蛋"],
        "calories": 220, "protein": 13,
        "fat": 14, "carbs": 12,
        "minutes": 15,
        "steps": "1. 番茄切塊、雞蛋打散。\\n2. 先炒蛋至半熟後盛起。\\n3. 炒番茄，再加入雞蛋拌炒。"
    },
    {
        "name": "雞肉蔬菜炒飯",
        "ingredients": ["雞肉", "白飯", "紅蘿蔔", "雞蛋"],
        "calories": 430, "protein": 28,
        "fat": 12, "carbs": 52,
        "minutes": 20,
        "steps": "1. 雞肉與蔬菜切丁。\\n2. 將雞肉炒熟。\\n3. 加入蔬菜、白飯及雞蛋拌炒。"
    },
    {
        "name": "高麗菜炒肉片",
        "ingredients": ["高麗菜", "豬肉"],
        "calories": 310, "protein": 24,
        "fat": 18, "carbs": 14,
        "minutes": 15,
        "steps": "1. 高麗菜洗淨切片。\\n2. 豬肉炒至熟透。\\n3. 加入高麗菜炒熟並調味。"
    },
    {
        "name": "香蕉燕麥牛奶",
        "ingredients": ["香蕉", "燕麥", "牛奶"],
        "calories": 320, "protein": 12,
        "fat": 8, "carbs": 52,
        "minutes": 5,
        "steps": "1. 香蕉切片。\\n2. 將燕麥、牛奶與香蕉混合。\\n3. 可依喜好冷藏或加熱。"
    },
    {
        "name": "蔬菜蛋花湯",
        "ingredients": ["雞蛋", "高麗菜", "紅蘿蔔"],
        "calories": 150, "protein": 10,
        "fat": 7, "carbs": 12,
        "minutes": 12,
        "steps": "1. 蔬菜切好後放入水中煮熟。\\n2. 雞蛋打散。\\n3. 倒入蛋液，煮至熟透。"
    }
]

# ---------- 初始化資料 ----------
if "foods" not in st.session_state:
    st.session_state.foods = [
        {"name": "番茄", "quantity": 3,
         "unit": "顆", "expiry": date.today() + timedelta(days=2)},
        {"name": "雞蛋", "quantity": 6,
         "unit": "顆", "expiry": date.today() + timedelta(days=7)},
        {"name": "高麗菜", "quantity": 1,
         "unit": "顆", "expiry": date.today() + timedelta(days=1)},
        {"name": "雞肉", "quantity": 300,
         "unit": "克", "expiry": date.today() + timedelta(days=3)}
    ]

if "meals" not in st.session_state:
    st.session_state.meals = []

foods = st.session_state.foods
today = date.today()

# ---------- 首頁統計 ----------
expiring = [
    f for f in foods
    if 0 <= (f["expiry"] - today).days <= 3
]
expired = [f for f in foods if f["expiry"] < today]

c1, c2, c3 = st.columns(3)
c1.metric("冰箱食材種類", f"{len(foods)} 種")
c2.metric("即將到期", f"{len(expiring)} 種")
c3.metric(
    "今日攝取熱量",
    f"{sum(m['calories'] for m in st.session_state.meals if m['date'] == today)} kcal"
)

if expired:
    st.error("以下食材已超過登記的保存期限，請先檢查是否變質，再決定是否丟棄。")
    st.write("、".join(f["name"] for f in expired))

elif expiring:
    st.warning(
        "優先檢查這些食材：" +
        "、".join(f["name"] for f in expiring)
    )

tab1, tab2, tab3, tab4 = st.tabs([
    "🧊 冰箱管理", "🍳 料理推薦", "📊 營養計算", "📅 飲食紀錄"
])

# ---------- 冰箱管理 ----------
with tab1:
    st.subheader("新增冰箱食材")

    with st.form("add_food", clear_on_submit=True):
        name = st.text_input("食材名稱")
        col1, col2 = st.columns(2)
        quantity = col1.number_input("數量", min_value=0.1, value=1.0)
        unit = col2.selectbox(
            "單位", ["個", "顆", "克", "公斤", "毫升", "包", "份"]
        )
        expiry = st.date_input(
            "保存期限", value=today + timedelta(days=3)
        )
        submitted = st.form_submit_button("新增食材")

        if submitted:
            if not name.strip():
                st.error("請先輸入食材名稱。")
            elif expiry < today:
                st.error("保存期限不能早於今天。")
            else:
                foods.append({
                    "name": name.strip(),
                    "quantity": quantity,
                    "unit": unit,
                    "expiry": expiry
                })
                st.success(f"已新增：{name.strip()}")
                st.rerun()

    st.subheader("目前的冰箱庫存")

    if foods:
        for i, food in enumerate(foods):
            days = (food["expiry"] - today).days
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.markdown(f"**{food['name']}**")
                col1.caption(f"數量：{food['quantity']:g} {food['unit']}")
                col2.write(f"期限：{food['expiry']}")
                if days < 0:
                    col2.error("已過登記期限")
                elif days <= 3:
                    col2.warning(f"{days} 天內到期")
                else:
                    col2.success(f"剩餘 {days} 天")
                if col3.button("刪除", key=f"delete_{i}"):
                    foods.pop(i)
                    st.rerun()
    else:
        st.info("冰箱目前沒有食材，請先新增。")

# ---------- 料理推薦 ----------
with tab2:
    st.subheader("依照現有食材推薦料理")

    if not foods:
        st.info("請先到冰箱管理新增食材。")
    else:
        available = {f["name"] for f in foods}
        results = []

        for recipe in RECIPES:
            matched = [
                ingredient for ingredient in recipe["ingredients"]
                if ingredient in available
            ]
            missing = [
                ingredient for ingredient in recipe["ingredients"]
                if ingredient not in available
            ]
            if matched:
                # 優先推薦使用快到期食材的料理
                urgent = sum(
                    1 for f in expiring if f["name"] in matched
                )
                score = len(matched) / len(recipe["ingredients"])
                results.append((urgent, score, recipe, matched, missing))

        results.sort(key=lambda x: (x[0], x[1]), reverse=True)

        if not results:
            st.info("目前沒有符合的料理，試著新增更多食材。")

        for urgent, score, recipe, matched, missing in results:
            with st.container(border=True):
                st.markdown(f"### 🍽️ {recipe['name']}")
                st.write(
                    f"符合食材：{'、'.join(matched)}"
                )
                st.write(
                    f"還缺少：{'、'.join(missing) if missing else '不缺食材！'}"
                )
                st.progress(score, text=f"食材符合度 {score:.0%}")
                st.caption(
                    f"約 {recipe['minutes']} 分鐘｜"
                    f"{recipe['calories']} kcal／份"
                )
                with st.expander("查看營養與料理步驟"):
                    st.write(
                        f"蛋白質 {recipe['protein']} g｜"
                        f"脂肪 {recipe['fat']} g｜"
                        f"碳水化合物 {recipe['carbs']} g"
                    )
                    st.markdown(recipe["steps"].replace("\\n", "\n"))

                if st.button("記錄這道料理", key=f"log_{recipe['name']}"):
                    st.session_state.meals.append({
                        "name": recipe["name"],
                        "date": today,
                        "calories": recipe["calories"],
                        "protein": recipe["protein"],
                        "fat": recipe["fat"],
                        "carbs": recipe["carbs"]
                    })
                    st.success("已加入今日飲食紀錄！")
                    st.rerun()

# ---------- 營養計算 ----------
with tab3:
    st.subheader("料理營養與熱量估算")

    selected = st.selectbox(
        "選擇料理", [r["name"] for r in RECIPES]
    )
    recipe = next(r for r in RECIPES if r["name"] == selected)
    servings = st.number_input(
        "食用份數", min_value=0.5, max_value=20.0,
        value=1.0, step=0.5
    )

    st.metric("總熱量", f"{recipe['calories'] * servings:.0f} kcal")
    a, b, c = st.columns(3)
    a.metric("蛋白質", f"{recipe['protein'] * servings:.1f} g")
    b.metric("脂肪", f"{recipe['fat'] * servings:.1f} g")
    c.metric("碳水化合物", f"{recipe['carbs'] * servings:.1f} g")

    st.caption("以上為範例估算值，實際營養會因食材重量、品牌及烹調用油而不同。")

# ---------- 飲食紀錄 ----------
with tab4:
    st.subheader("今日與歷史飲食紀錄")
    meals = st.session_state.meals

    if meals:
        df = pd.DataFrame(meals)
        st.dataframe(
            df.rename(columns={
                "name": "料理",
                "date": "日期",
                "calories": "熱量(kcal)",
                "protein": "蛋白質(g)",
                "fat": "脂肪(g)",
                "carbs": "碳水化合物(g)"
            }),
            use_container_width=True,
            hide_index=True
        )

        daily = df.groupby("date")["calories"].sum()
        st.subheader("每日熱量統計")
        st.bar_chart(daily)
        st.metric("累積記錄熱量", f"{df['calories'].sum():.0f} kcal")

        if st.button("清除全部飲食紀錄"):
            st.session_state.meals = []
            st.rerun()
    else:
        st.info("目前還沒有飲食紀錄，請到料理推薦頁記錄料理。")

st.divider()
st.caption(
    "智慧美食與冰箱管理｜30 天剩食料理推薦與營養熱量計算專題"
)
