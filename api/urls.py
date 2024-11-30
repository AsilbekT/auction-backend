from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, OwnerViewSet, LegalProceedingViewSet, AuctionViewSet, SalesInformationViewSet, ConnectionViewSet, MortgageAndDebtViewSet, TaxLienViewSet

router = DefaultRouter()
router.register('properties', PropertyViewSet)
router.register('owners', OwnerViewSet)
router.register('legal-proceedings', LegalProceedingViewSet)
router.register('auctions', AuctionViewSet)
router.register('sales-information', SalesInformationViewSet)
router.register('connections', ConnectionViewSet)
router.register('mortgages-and-debts', MortgageAndDebtViewSet)
router.register('tax-liens', TaxLienViewSet)

urlpatterns = router.urls
