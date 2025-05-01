from django.contrib import admin
from .models import Category, Product, Wallet

admin.site.register(Category)
admin.site.register(Product)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
    list_editable = ('balance',)
    
admin.site.register(Wallet, WalletAdmin)