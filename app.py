import streamlit as st
import pandas as pd
import json
import os

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="Dragon Store - دراگون استور",
    page_icon="🐉",
    layout="wide"
)

# --- 2. حقن تنسيقات الـ CSS (الخلفية المتدرجة والتنسيقات الفخمة) ---
st.markdown(
    """
    <style>
    /* خلفية متدرجة فخمة للمتجر */
    .stApp {
        background: linear-gradient(135deg, #4a0e17 0%, #2b0609 50%, #150204 100%);
        color: #ffffff;
    }
    
    /* تنسيقات عامة للنصوص والأزرار */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. إدارة البيانات والملفات (الطلبات والمنتجات) ---
ORDERS_FILE = "orders_db.json"
PRODUCTS_FILE = "products_db.json"

def load_json(file_path, default_val):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_val
    return default_val

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

orders_db = load_json(ORDERS_FILE, {})
products_db = load_json(PRODUCTS_FILE, {})

# --- 4. القائمة الجانبية (Navigation) ---
st.sidebar.title("🎮 قائمة المتجر الأسطوري")
page = st.sidebar.radio("الانتقال إلى:", ["الرئيسية والمتجر 🛒", "تتبع الطلب 📦", "لوحة الأدمن 🛠️"])

# --- صفحة المتجر الرئيسية ---
if page == "الرئيسية والمتجر 🛒":
    st.title("🐉 متجر الأناقة الأسطورية - Dragon Store")
    st.write("أهلاً بك يا بطل! تصفح أحدث المنتجات واطلب ما تحب بكل سهولة.")
    
    if not products_db:
        st.info("📦 الكتالوج فارغ حالياً. يمكن للأدمن إضافة منتجات جديدة من لوحة التحكم.")
    else:
        for p_id, p_info in products_db.items():
            st.markdown(f"### {p_info.get('name')}")
            st.write(f"💰 السعر: {p_info.get('price')} ج.م")
            st.write(f"📌 القسم: {p_info.get('category')}")
            st.markdown("---")

# --- صفحة تتبع الطلب ---
elif page == "تتبع الطلب 📦":
    st.markdown("## 📦 تتبع حالة طلبك (Order Tracking)")
    st.write("أدخل رقم الطلب أو رقم الهاتف المسجل لمتابعة شحنتك لحظة بلحظة:")
    
    search_query = st.text_input("🔍 أدخل رقم الطلب أو الهاتف:", placeholder="مثال: ORD-1001 أو 01558478544")
    
    if st.button("بحث عن الطلب 🚀"):
        if search_query.strip():
            found = False
            for order_id, details in orders_db.items():
                if search_query.strip() == order_id or search_query.strip() == details.get("phone"):
                    found = True
                    st.success(f"📌 **رقم الطلب:** {order_id}")
                    status = details.get("status", "قيد المعالجة ⏳")
                    
                    if "قيد المعالجة" in status:
                        st.warning(f"**حالة الشحن:** {status}")
                    elif "جاري الشحن" in status:
                        st.info(f"**حالة الشحن:** {status}")
                    else:
                        st.success(f"**حالة الشحن:** {status}")
                        
                    st.write(f"👤 **العميل:** {details.get('name')}")
                    st.write(f"📍 **العنوان:** {details.get('address')}")
                    st.write(f"💰 **الإجمالي:** {details.get('total')} ج.م")
                    st.markdown("---")
            if not found:
                st.error("❌ لم يتم العثور على أي طلب بهذه البيانات.")
        else:
            st.warning("الرجاء كتابة رقم الطلب أو الهاتف أولاً.")

# --- لوحة تحكم الأدمن ---
elif page == "لوحة الأدمن 🛠️":
    st.title("🛠️ لوحة تحكم الأدمن (Admin Dashboard)")
    
    admin_pass = st.text_input("كلمة مرور الأدمن:", type="password")
    if admin_pass == "12345":
        st.success("تم تسجيل الدخول بنجاح يا أدمن! 👑")
        
        tab1, tab2 = st.tabs(["إدارة المنتجات 👕", "إدارة الطلبات والشحن 📦"])
        
        with tab1:
            st.subheader("➕ إضافة منتج جديد")
            p_name = st.text_input("اسم المنتج")
            p_price = st.number_input("السعر بالجنيه", min_value=0.0)
            p_cat = st.selectbox("القسم", ["هوديس وملابس", "أكسسوارات", "عطور"])
            
            if st.button("حفظ وإضافة المنتج"):
                if p_name:
                    p_id = str(len(products_db) + 1001)
                    products_db[p_id] = {"name": p_name, "price": p_price, "category": p_cat}
                    save_json(PRODUCTS_FILE, products_db)
                    st.success("تم إضافة المنتج بنجاح!")
                else:
                    st.warning("أدخل اسم المنتج من فضلك.")
                    
        with tab2:
            st.subheader("📋 تحديث حالات الطلبات الحالية")
            if not orders_db:
                st.info("لا توجد طلبات مسجلة حتى الآن.")
            else:
                for o_id, o_det in orders_db.items():
                    with st.expander(f"طلب: {o_id} - {o_det.get('name')}"):
                        current_status = o_det.get("status", "قيد المعالجة ⏳")
                        new_stat = st.selectbox(
                            "تحديث الحالة:",
                            ["قيد المعالجة ⏳", "جاري الشحن 🚚", "تم التوصيل ✅"],
                            index=["قيد المعالجة ⏳", "جاري الشحن 🚚", "تم التوصيل ✅"].index(current_status),
                            key=f"st_{o_id}"
                        )
                        if st.button("تحديث", key=f"btn_{o_id}"):
                            orders_db[o_id]["status"] = new_stat
                            save_json(ORDERS_FILE, orders_db)
                            st.success("تم التحديث بنجاح!")
    elif admin_pass != "":
        st.error("كلمة المرور غير صحيحة! (كلمة المرور الافتراضية هي: 12345)")