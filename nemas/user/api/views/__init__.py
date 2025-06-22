from .user_views import (
    CreateUserView,
    CreateTokenView,
    CreateSuperUserView,
    ManageUserView,
    ManageRefreshTokenView,
    ManageVerifyTokenView,
    GETUserProfileByPhoneNumberView,
)

from .user_prop_view import (
    UserPropView,
)

from .user_verification_view import (
    UserKtpView,
    CreateKtpIfNotVerify,
    CreateComparePhotoANDKtp,
)


from .user_pin_view import (
    UserPinView,
)
from .user_reset_token_view import RequestResetView, ResetView

from .user_address_view import UserAddressView

from .user_notification_view import (
    user_notification_views,
)

from .user_notification_price_views import user_notification_price_views
