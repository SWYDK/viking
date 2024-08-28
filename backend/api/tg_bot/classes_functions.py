from aiogram.fsm.state import State, StatesGroup


# все необходимые стейты для фсм
class Admin(StatesGroup):
    mailing_state = State()
    mailing_text = State()
    mailing_text_only = State()
    ask = State()
    confirm_yes = State()
    confirm_no = State()

    p_name = State()
    p_photo1 = State()
    p_photo2 = State()
    p_photo3 = State()
    p_photo4 = State()
    p_photo5 = State()
    p_photo6 = State()
    p_photo7 = State()
    p_photo8 = State()
    p_photo9 = State()
    p_photo10 = State()


    p_desc = State()
    p_capacity = State()
    p_price = State()


    s_type1 = State()
    s_type2 = State()
    s_type3 = State()
    s_name = State()
    s_photo = State()
    s_desc = State()
    s_weight = State()
    s_kitchen = State()
    s_compound = State()

    s_price = State()

    time_data = State()
    number = State()

    confirm = State()
    payment = State()
    comment = State()
    check = State()
