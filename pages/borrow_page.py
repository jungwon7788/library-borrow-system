# pages/borrow_page.py
import streamlit as st
from datetime import date, timedelta

import model
import controller


# =========================
# Helper functions
# =========================
def _contains_ignore_case(series, keyword: str):
    kw = (keyword or "").strip().lower()
    if not kw:
        return series.notna()
    return series.fillna("").astype(str).str.lower().str.contains(kw)


# =========================
# Main render function
# =========================
def render_borrow():
    st.subheader("🔄 การทำรายการยืม-คืนหนังสือ")

    # สร้าง schema ยืม-คืน หากยังไม่มี
    model.ensure_borrow_schema()

    # ผู้ทำรายการ (admin/staff)
    user = st.session_state.get("user") or {}
    staff_user_id = user.get("id")

    # ==================================================
    # ส่วนที่ 1: ทำรายการยืม
    # ==================================================
    st.markdown("### 1) ทำรายการยืม (ยืมได้มากกว่าหนึ่งเล่มต่อครั้ง)")

    members_df = model.get_active_members()
    if members_df.empty:
        st.warning("ไม่พบสมาชิกที่ใช้งานอยู่ กรุณาเพิ่มสมาชิกก่อนทำรายการยืม")
        return

    # ---------- 1.1 เลือกสมาชิก ----------
    st.markdown("**1.1 เลือกสมาชิก (ค้นหาจากรหัสสมาชิกหรือชื่อสมาชิก)**")
    member_kw = st.text_input(
        "ค้นหาสมาชิก",
        placeholder="พิมพ์รหัสสมาชิก หรือ ชื่อสมาชิก เช่น M010 หรือ Martha",
        key="borrow_member_kw",
    )

    mdf = members_df.copy()
    mask_m = (
        _contains_ignore_case(mdf["member_code"], member_kw)
        | _contains_ignore_case(mdf["name"], member_kw)
    )
    mdf = mdf[mask_m].copy()

    if mdf.empty:
        st.info("ไม่พบสมาชิกตามคำค้น กรุณาลองใหม่")
        selected_member_id = None
    else:
        member_options = {
            f"{r['member_code']} : {r['name']}": int(r["id"])
            for _, r in mdf.iterrows()
        }
        member_label = st.selectbox(
            "รายการสมาชิกที่พบ",
            list(member_options.keys()),
            key="borrow_member_select",
        )
        selected_member_id = member_options.get(member_label)

    st.markdown("---")

    # ---------- 1.2 เพิ่มหนังสือ (ตะกร้ายืม) ----------
    st.markdown("**1.2 เพิ่มรายการหนังสือ (ค้นหาและเพิ่มทีละรายการ)**")

    if "borrow_cart" not in st.session_state:
        st.session_state["borrow_cart"] = []

    books_df = model.get_available_books()

    if books_df.empty:
        st.info("ขณะนี้ไม่มีหนังสือสถานะ available สำหรับให้ยืม")
    else:
        book_kw = st.text_input(
            "ค้นหาหนังสือ",
            placeholder="พิมพ์รหัสหนังสือ หรือ ชื่อหนังสือ",
            key="borrow_book_kw",
        )

        bdf = books_df.copy()
        kw = (book_kw or "").strip()
        if kw:
            mask_id = bdf["id"].astype(str).str.contains(kw, na=False)
            mask_title = bdf["title"].astype(str).str.contains(kw, case=False, na=False)
            bdf = bdf[mask_id | mask_title].copy()

        if bdf.empty:
            st.info("ไม่พบหนังสือตามคำค้น กรุณาลองใหม่")
        else:
            book_options = {
                f"{int(r['id'])} : {r['title']}": int(r["id"])
                for _, r in bdf.iterrows()
            }
            book_label = st.selectbox(
                "รายการหนังสือที่พบ",
                list(book_options.keys()),
                key="borrow_book_select",
            )
            add_book_id = book_options.get(book_label)

            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("➕ เพิ่มรายการ", use_container_width=True):
                    if add_book_id in st.session_state["borrow_cart"]:
                        st.warning("หนังสือเล่มนี้ถูกเพิ่มในรายการแล้ว")
                    else:
                        st.session_state["borrow_cart"].append(int(add_book_id))
                        st.success("เพิ่มรายการเรียบร้อยแล้ว")
                        st.rerun()

            with col2:
                if st.button("🧹 ล้างรายการที่เลือกทั้งหมด", use_container_width=True):
                    st.session_state["borrow_cart"] = []
                    st.rerun()

    # ---------- แสดงตะกร้ายืม ----------
    if st.session_state["borrow_cart"]:
        cart_ids = st.session_state["borrow_cart"]
        cart_df = books_df[books_df["id"].isin(cart_ids)].copy().sort_values("id")

        st.markdown("**รายการหนังสือที่เลือก (ตะกร้ายืม)**")
        st.dataframe(cart_df[["id", "title", "author"]], use_container_width=True)

        st.markdown("**ลบรายการทีละเล่ม**")
        for _, r in cart_df.iterrows():
            bid = int(r["id"])
            c1, c2 = st.columns([6, 1])
            with c1:
                st.write(f"📘 {bid} : {r['title']}")
            with c2:
                if st.button("ลบ", key=f"remove_cart_{bid}"):
                    st.session_state["borrow_cart"] = [
                        x for x in st.session_state["borrow_cart"] if int(x) != bid
                    ]
                    st.rerun()
    else:
        st.info("ยังไม่มีรายการหนังสือในตะกร้ายืม")

    # ---------- 1.3 กำหนดส่ง + บันทึก ----------
    default_due = date.today() + timedelta(days=7)
    due_date = st.date_input(
        "กำหนดส่ง (ค่าเริ่มต้นของรายการ)",
        value=default_due,
        key="borrow_due",
    )
    note = st.text_input(
        "หมายเหตุ (ถ้ามี)",
        placeholder="ตัวอย่าง: ยืมเพื่อทำรายงาน",
        key="borrow_note",
    )

    can_submit = bool(selected_member_id) and bool(st.session_state["borrow_cart"])
    if st.button("✅ บันทึกการยืม", disabled=not can_submit, use_container_width=True):
        ok, msgs, _ = controller.borrow_books(
            member_id=selected_member_id,
            staff_user_id=staff_user_id,
            due_date_iso=due_date.isoformat() if due_date else None,
            book_ids=[int(x) for x in st.session_state["borrow_cart"]],
            note=note.strip() if note else None,
        )
        if not ok:
            for m in msgs:
                st.error("⚠ " + m)
        else:
            for m in msgs:
                st.success("✅ " + m)
            st.session_state["borrow_cart"] = []
            st.rerun()

    st.divider()

    # ==================================================
    # ส่วนที่ 2: ทำรายการคืน
    # ==================================================
    st.markdown("### 2) ทำรายการคืน")

    st.markdown("**2.1 เลือกสมาชิกเพื่อดูรายการค้างส่ง**")
    return_member_kw = st.text_input(
        "ค้นหาสมาชิก (สำหรับคืน)",
        placeholder="พิมพ์รหัสสมาชิก หรือ ชื่อสมาชิก",
        key="return_member_kw",
    )

    rdf = members_df.copy()
    mask_rm = (
        _contains_ignore_case(rdf["member_code"], return_member_kw)
        | _contains_ignore_case(rdf["name"], return_member_kw)
    )
    rdf = rdf[mask_rm].copy()

    if rdf.empty:
        st.info("ไม่พบสมาชิกตามคำค้น กรุณาลองใหม่")
        return_member_id = None
    else:
        return_member_options = {
            f"{r['member_code']} : {r['name']}": int(r["id"])
            for _, r in rdf.iterrows()
        }
        return_member_label = st.selectbox(
            "รายการสมาชิกที่พบ (สำหรับคืน)",
            list(return_member_options.keys()),
            key="return_member_select",
        )
        return_member_id = return_member_options.get(return_member_label)

    if return_member_id:
        active_member_df = model.get_active_borrow_items_by_member(return_member_id)

        if active_member_df.empty:
            st.info("สมาชิกคนนี้ไม่มีรายการยืมค้างส่ง")
        else:
            st.markdown("**2.2 เลือกรายการที่ต้องการคืน**")
            show_df = active_member_df.copy()
            show_df.insert(0, "คืน", False)

            edited = st.data_editor(
                show_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "คืน": st.column_config.CheckboxColumn("คืน")
                },
                disabled=[c for c in show_df.columns if c != "คืน"],
            )

            selected_item_ids = (
                edited.loc[edited["คืน"] == True, "item_id"]
                .astype(int)
                .tolist()
            )

            if st.button(
                "📥 ยืนยันการคืนรายการที่เลือก",
                use_container_width=True,
                disabled=len(selected_item_ids) == 0,
            ):
                ok, msgs = controller.return_book_items(
                    item_ids=selected_item_ids,
                    return_staff_user_id=staff_user_id,
                )
                if not ok:
                    for m in msgs:
                        st.error("⚠ " + m)
                else:
                    for m in msgs:
                        st.success("✅ " + m)
                    st.rerun()

    st.divider()

    # ==================================================
    # ส่วนที่ 3: รายการค้างส่งทั้งหมด
    # ==================================================
    st.markdown("### 3) รายการหนังสือค้างส่งทั้งหมด")

    all_active_df = model.get_active_borrow_items()

    if all_active_df.empty:
        st.info("ไม่พบรายการหนังสือค้างส่ง")
    else:
        show_cols = [
            "รหัสสมาชิก", "ชื่อสมาชิก",
            "รหัสหนังสือ", "ชื่อหนังสือ",
            "วันที่ยืม", "กำหนดส่ง",
            "ผู้ทำรายการยืม", "บทบาทผู้ทำรายการ",
        ]
        show_cols = [c for c in show_cols if c in all_active_df.columns]

        st.dataframe(all_active_df[show_cols], use_container_width=True)

    st.divider()

    # ==================================================
    # ส่วนที่ 4: ประวัติการยืม-คืน
    # ==================================================
    st.markdown("### 4) ประวัติการยืม-คืน")

    history_df = model.get_borrow_history(limit=200)

    if history_df.empty:
        st.info("ยังไม่มีประวัติการยืม-คืน")
    else:
        hist_kw = st.text_input(
            "ค้นหาประวัติ",
            placeholder="พิมพ์ชื่อหนังสือ / รหัสสมาชิก / ชื่อสมาชิก",
            key="history_search_kw",
        ).strip()

        df = history_df.copy()

        drop_cols = [
            c for c in df.columns
            if c in ("item_id", "tx_id") or "บทบาท" in c
        ]
        if drop_cols:
            df = df.drop(columns=drop_cols, errors="ignore")

        if hist_kw:
            kw = hist_kw.lower()
            mask = (
                df.get("ชื่อหนังสือ", "").astype(str).str.lower().str.contains(kw, na=False)
                | df.get("รหัสสมาชิก", "").astype(str).str.lower().str.contains(kw, na=False)
                | df.get("ชื่อสมาชิก", "").astype(str).str.lower().str.contains(kw, na=False)
            )
            df = df[mask].copy()

        if df.empty:
            st.info("ไม่พบข้อมูลตามคำค้น")
        else:
            st.dataframe(df, use_container_width=True)
