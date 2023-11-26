from sqlalchemy import ForeignKey, INTEGER, asc, func, case
from sqlalchemy.orm import relationship

from app.enums import STATUS_ASSIGNEE, GROUP_KEY, OVERALL_STATUS
from app.extensions import db
from app.utils import get_timestamp_now


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    full_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    group_id = db.Column(ForeignKey('group.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    created_date = db.Column(db.Integer, default=get_timestamp_now())
    modified_date = db.Column(db.Integer, default=0)
    last_modified_user = db.Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'))
    created_user = db.Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'))
    is_active = db.Column(db.Boolean, default=1)  # 1: Mở tài khoản , 0: Khóa tài khoản
    group = relationship('Group', primaryjoin='Group.id == User.group_id')


    @property
    def done_original_number(self):
        if self.group.key == GROUP_KEY['user']:
            done_original_number = ProductUser.query.filter(
                ProductUser.status_assignee == STATUS_ASSIGNEE['done_original'],
                ProductUser.assignee == self.id).count()
        else:
            done_original_number = 0
        return done_original_number

    @property
    def pending_number(self):
        if self.group.key == GROUP_KEY['user']:
            pending_number = ProductUser.query.filter(
                ProductUser.status_assignee == STATUS_ASSIGNEE['pending'],
                ProductUser.assignee == self.id).count()
        else:
            pending_number = 0
        return pending_number

    @property
    def failed_number(self):
        if self.group.key == GROUP_KEY['user']:
            failed_number = ProductUser.query.filter(
                ProductUser.status_assignee == STATUS_ASSIGNEE['failed'],
                ProductUser.assignee == self.id).count()
        else:
            failed_number = 0
        return failed_number

    @property
    def reviewing_number(self):
        if self.group.key == GROUP_KEY['user']:
            reviewing_number = ProductUser.query.filter(
                ProductUser.status_assignee == STATUS_ASSIGNEE['reviewing'],
                ProductUser.assignee == self.id).count()
        else:
            reviewing_number = Product.query.filter(Product.overall_status == OVERALL_STATUS['reviewing'],
                                                    ProductUser.assignee == self.id).count()
        return reviewing_number

    @property
    def done_number(self):
        if self.group.key == GROUP_KEY['user']:
            done_number = ProductUser.query.filter(
                ProductUser.status_assignee == STATUS_ASSIGNEE['done'],
                ProductUser.assignee == self.id).count()
        else:
            done_number = Product.query.filter(Product.overall_status == OVERALL_STATUS['done'],
                                               ProductUser.assignee == self.id).count()
        return done_number


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.String(50), primary_key=True)
    key = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    type = db.Column(db.SmallInteger, default=1)  # tổng của 4 loại quyền sau 1: Xem, 2: Thêm, 4: Sửa, 8: Xóa
    created_date = db.Column(db.Integer, default=get_timestamp_now())
    modified_date = db.Column(db.Integer, default=0)

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.String(50), primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=False)
    resource = db.Column(db.String(500), nullable=False, unique=False)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.String(50), primary_key=True)
    key = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500))
    created_date = db.Column(db.Integer, default=get_timestamp_now(), nullable=False, index=True)
    modified_date = db.Column(db.Integer, default=0)

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(db.String(50), primary_key=True)
    role_id = db.Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    permission_id = db.Column(ForeignKey('permission.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                              index=True)

    permission = relationship('Permission', primaryjoin='RolePermission.permission_id == Permission.id')
    role = relationship('Role', primaryjoin='RolePermission.role_id == Role.id')


class GroupRole(db.Model):
    __tablename__ = 'group_role'

    id = db.Column(db.String(50), primary_key=True)
    role_id = db.Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    group_id = db.Column(ForeignKey('group.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    role = relationship('Role', primaryjoin='GroupRole.role_id == Role.id')

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


# product có 2 bản assignee và 1 bản ocr ( không có trong bảng ProductUser,
# lưu trong ProductColor theo product_id, assignee là None)


class Product(db.Model):
    __tablename__ = 'product'
    # id = db.Column(db.String(50), primary_key=True)
    id = db.Column(db.String(50), primary_key=True)
    product_order = db.Column(db.String(50))
    customer = db.Column(db.String(200))
    date = db.Column(db.DATE)
    dm = db.Column(db.String(25))

    overall_status = db.Column(db.SmallInteger, default=0)
    reviewer = db.Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True,
                         index=True)

    link = db.Column(db.String(250))
    created_date = db.Column(db.Integer)
    modified_date = db.Column(db.Integer, default=0)

    users_assignee = relationship('ProductUser', primaryjoin='and_(ProductUser.product_id == Product.id, '
                                                             'ProductUser.assignee.is_not(None))')
    product_colors = relationship('ProductColor', primaryjoin='ProductColor.product_id == Product.id',
                                  order_by='asc(ProductColor.ordinal_nr)')
    user_reviewer = relationship('User', primaryjoin='User.id == Product.reviewer')


class ProductUser(db.Model):
    __tablename__ = 'product_user'

    id = db.Column(db.String(50), primary_key=True)
    status_assignee = db.Column(db.SmallInteger)
    product_order = db.Column(db.String(50))
    customer = db.Column(db.String(200))
    date = db.Column(db.DATE)
    dm = db.Column(db.String(25))
    product_designation = db.Column(db.String(50))
    assignee = db.Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True,
                         index=True)
    speed = db.Column(db.String(25))
    linear_meters = db.Column(db.String(25))
    center_line = db.Column(db.String(25))
    deductions = db.Column(db.String(25))
    Name_FM = db.Column(db.String(50))
    Name_FM_1 = db.Column(db.String(50))
    Name_FM_2 = db.Column(db.String(50))
    # created_date = db.Column(db.Integer, default=get_timestamp_now())
    # modified_date = db.Column(db.Integer, default=0)
    product_id = db.Column(ForeignKey('product.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True,
                           index=True)
    index_assignee = db.Column(db.SmallInteger, default=1)

    user = relationship('User', primaryjoin='User.id == ProductUser.assignee')

    @property
    def product_color(self):
        product_color = ProductColor.query.filter(ProductColor.product_id == self.product_id,
                                                  ProductColor.assignee == self.assignee) \
            .order_by(asc(ProductColor.ordinal_nr)).all()
        return product_color


class ProductColor(db.Model):
    __tablename__ = 'product_color'
    id = db.Column(db.String(50), primary_key=True)
    product_id = db.Column(ForeignKey('product.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True,
                           index=True)
    color = db.Column(db.String(50))
    ordinal_nr = db.Column(db.SmallInteger, nullable=False, unique=False)
    assignee = db.Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True,
                         index=True)
    pressurdr_number = db.Column(db.Float())
    quantity_on_release = db.Column(db.Float())
    aftersets_additions = db.Column(db.Float())
    decrease = db.Column(db.Float())
    approach_colorimetry = db.Column(db.Float())
    quantity_at_FG = db.Column(db.Float())
    sub_add = db.Column(db.Float())
    decrease_kg = db.Column(db.Float())
    consumption_kg = db.Column(db.Float())

    # created_date = db.Column(db.Integer, default=get_timestamp_now())
    # modified_date = db.Column(db.Integer, default=0)

    color_test = relationship('ColorTest', primaryjoin='ProductColor.id == ColorTest.product_color_id',
                              order_by='asc(ColorTest.test)')


class ColorTest(db.Model):
    __tablename__ = 'color_test'
    id = db.Column(db.String(50), primary_key=True)
    product_color_id = db.Column(ForeignKey('product_color.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True,
                                 index=True)
    test = db.Column(INTEGER(), nullable=False)
    viscosity = db.Column(db.Float())
    water = db.Column(db.Float())
    offcut = db.Column(db.Float())
    Blend_conc = db.Column(db.Float())
    yellow_org = db.Column(db.Float())
    yellow_reddish = db.Column(db.Float())
    oxide_yellow = db.Column(db.Float())
    yellow_greenish = db.Column(db.Float())
    red = db.Column(db.Float())
    red_bluish = db.Column(db.Float())
    blue = db.Column(db.Float())
    black = db.Column(db.Float())
    white = db.Column(db.Float())
    supplements = db.Column(db.Float())
    speed = db.Column(db.Float())
    paper_type_UR = db.Column(db.Float())
    paper_type_current = db.Column(db.Float())
    paper_type_LL = db.Column(db.Float())
    visko_UR = db.Column(db.Float())
    visko_LL = db.Column(db.Float())
    ESA_UR = db.Column(db.Float())
    ESA_current = db.Column(db.Float())
    ESA_LL = db.Column(db.Float())

    # created_date = db.Column(db.Integer, default=get_timestamp_now())
    # modified_date = db.Column(db.Integer, default=0)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(255))
    show = db.Column(db.Boolean, default=0)
    duration = db.Column(db.Integer, default=5)
    status = db.Column(db.String(20), default='success')
    message = db.Column(db.String(500), nullable=False)
    dynamic = db.Column(db.Boolean, default=0)
    object = db.Column(db.String(255))


class ProductColorFinal(db.Model):
    __tablename__ = 'product_color_final'
    id = db.Column(db.String(50), primary_key=True)
    product_id = db.Column(ForeignKey('product_final.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True,
                           index=True)
    color = db.Column(db.String(50))
    ordinal_nr = db.Column(db.SmallInteger, nullable=False, unique=False)
    pressurdr_number = db.Column(db.Float())
    quantity_on_release = db.Column(db.Float())
    aftersets_additions = db.Column(db.Float())
    decrease = db.Column(db.Float())
    approach_colorimetry = db.Column(db.Float())
    quantity_at_FG = db.Column(db.Float())
    sub_add = db.Column(db.Float())
    decrease_kg = db.Column(db.Float())
    consumption_kg = db.Column(db.Float())

    color_test = relationship('ColorTestFinal', primaryjoin='ProductColorFinal.id == ColorTestFinal.product_color_id',
                              order_by='asc(ColorTestFinal.test)')


class ColorTestFinal(db.Model):
    __tablename__ = 'color_test_final'
    id = db.Column(db.String(50), primary_key=True)
    product_color_id = db.Column(ForeignKey('product_color_final.id', ondelete='SET NULL', onupdate='CASCADE'),
                                 nullable=True,
                                 index=True)
    test = db.Column(INTEGER(), nullable=False)
    viscosity = db.Column(db.Float())
    water = db.Column(db.Float())
    offcut = db.Column(db.Float())
    Blend_conc = db.Column(db.Float())
    yellow_org = db.Column(db.Float())
    yellow_reddish = db.Column(db.Float())
    oxide_yellow = db.Column(db.Float())
    yellow_greenish = db.Column(db.Float())
    red = db.Column(db.Float())
    red_bluish = db.Column(db.Float())
    blue = db.Column(db.Float())
    black = db.Column(db.Float())
    white = db.Column(db.Float())
    supplements = db.Column(db.Float())
    speed = db.Column(db.Float())
    paper_type_UR = db.Column(db.Float())
    paper_type_current = db.Column(db.Float())
    paper_type_LL = db.Column(db.Float())
    visko_UR = db.Column(db.Float())
    visko_LL = db.Column(db.Float())
    ESA_UR = db.Column(db.Float())
    ESA_current = db.Column(db.Float())
    ESA_LL = db.Column(db.Float())


class ProductFinal(db.Model):
    __tablename__ = 'product_final'
    # id = db.Column(db.String(50), primary_key=True)
    id = db.Column(db.String(50), primary_key=True)
    product_order = db.Column(db.String(50))
    product_designation = db.Column(db.String(50))
    customer = db.Column(db.String(200))
    date = db.Column(db.DATE)

    speed = db.Column(db.String(25))
    linear_meters = db.Column(db.String(25))
    center_line = db.Column(db.String(25))
    deductions = db.Column(db.String(25))
    Name_FM = db.Column(db.String(50))
    Name_FM_1 = db.Column(db.String(50))
    Name_FM_2 = db.Column(db.String(50))
    dm = db.Column(db.String(25))
    link = db.Column(db.String(250))
    created_date = db.Column(db.Integer)
    modified_date = db.Column(db.Integer, default=0)

    reviewer = db.Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True,
                         index=True)

    product_color = relationship('ProductColorFinal', primaryjoin='ProductColorFinal.product_id == ProductFinal.id',
                                  order_by='asc(ProductColorFinal.ordinal_nr)')
