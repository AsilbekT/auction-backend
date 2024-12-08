from rest_framework.routers import DefaultRouter
from .views import (
        EmailViewSet,
        LeadViewSet,
        PhoneViewSet,
        PropertyViewSet, 
        OwnerViewSet, 
        LegalProceedingViewSet,
        AuctionViewSet,
        SalesInformationViewSet,
        ConnectionViewSet,
        MortgageAndDebtViewSet,
        TaxLienViewSet,
        DuplicateCheckViewSet
    )

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'legal-proceedings', LegalProceedingViewSet)
router.register(r'auctions', AuctionViewSet)
router.register(r'sales-information', SalesInformationViewSet)
router.register(r'connections', ConnectionViewSet)
router.register(r'mortgages-and-debts', MortgageAndDebtViewSet)
router.register(r'tax-liens', TaxLienViewSet)
router.register(r'duplicate-checks', DuplicateCheckViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'phones', PhoneViewSet)
router.register(r'emails', EmailViewSet)

urlpatterns = router.urls
