# Generated by Django 5.1.3 on 2024-12-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DublicateCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('reformated_address', models.CharField(max_length=255)),
                ('source_name', models.CharField(choices=[('Auction', 'auction.com'), ('Foreclosure', 'foreclosure.com'), ('Salesweb', 'salesweb'), ('Realtybid', 'realtybid'), ('Njcourt', 'njcourt'), ('Bids', 'bids'), ('FL', 'fl'), ('Xome', 'xome'), ('ASAP', 'asap')], max_length=20)),
                ('auction', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='auction',
            name='event_id',
        ),
        migrations.AlterField(
            model_name='auction',
            name='auction_date',
            field=models.DateField(blank=True, help_text='The date on which the auction will take place', null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='estimated_debt',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total estimated debt associated with the property', max_digits=12),
        ),
        migrations.AlterField(
            model_name='auction',
            name='estimated_resale_value',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The estimated resale value of the property at auction', max_digits=12),
        ),
        migrations.AlterField(
            model_name='auction',
            name='opening_bid',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Starting bid for the auction', max_digits=12),
        ),
        migrations.AlterField(
            model_name='auction',
            name='rental_estimate',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Estimated rental income the property could generate', max_digits=10),
        ),
        migrations.AlterField(
            model_name='auction',
            name='trustee_sale_number',
            field=models.CharField(blank=True, help_text='A unique identifier assigned to the trustee sale', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='case_type',
            field=models.CharField(blank=True, choices=[('FC', 'Foreclosure'), ('LN', 'Lien')], help_text='The type of legal case, e.g., Foreclosure or Lien', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='date_of_filing',
            field=models.DateField(blank=True, help_text='The date on which the legal case was filed', null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='defendants',
            field=models.TextField(blank=True, help_text='Text field containing the names of all defendants', null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='equity',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Equity amount involved in the legal proceeding', max_digits=12),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='plaintiff',
            field=models.CharField(blank=True, help_text='The plaintiff in the legal case', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='plaintiff_attorney_firm',
            field=models.CharField(blank=True, help_text='The law firm representing the plaintiff', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='plaintiff_attorney_name',
            field=models.CharField(blank=True, help_text='The name of the attorney representing the plaintiff', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='plaintiff_atty_bar_no',
            field=models.CharField(blank=True, help_text="Bar number of the plaintiff's attorney", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='probate_case_number',
            field=models.CharField(blank=True, help_text='Case number if the legal proceeding is a probate case', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='legalproceeding',
            name='total_amount_owed',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The total amount owed in the case', max_digits=12),
        ),
        migrations.AlterField(
            model_name='mortgageanddebt',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The interest rate of the mortgage', max_digits=5),
        ),
        migrations.AlterField(
            model_name='mortgageanddebt',
            name='lender_name',
            field=models.CharField(blank=True, help_text='The name of the lender', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mortgageanddebt',
            name='loan_type',
            field=models.CharField(blank=True, choices=[('PR', 'Primary'), ('SC', 'Secondary')], help_text='The type of loan, e.g., Primary, Secondary', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='mortgageanddebt',
            name='mortgage_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The amount of the mortgage', max_digits=12),
        ),
        migrations.AlterField(
            model_name='mortgageanddebt',
            name='mortgage_date',
            field=models.DateField(blank=True, help_text='The date the mortgage was registered', null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='first_name',
            field=models.CharField(blank=True, help_text='The first name of the property owner', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='apn',
            field=models.CharField(blank=True, help_text="The assessor's parcel number, unique identifier for the property", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='baths',
            field=models.FloatField(default=0, help_text='Number of bathrooms in the property'),
        ),
        migrations.AlterField(
            model_name='property',
            name='beds',
            field=models.IntegerField(default=0, help_text='Number of bedrooms in the property'),
        ),
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.CharField(blank=True, help_text='The city where the property is located', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='county',
            field=models.CharField(blank=True, help_text='The county where the property is located', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='lot_size',
            field=models.FloatField(default=0, help_text='The size of the property lot in square feet'),
        ),
        migrations.AlterField(
            model_name='property',
            name='occupancy_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(blank=True, choices=[('SF', 'Single Family'), ('MF', 'Multi Family'), ('CM', 'Commercial')], help_text='The type of property, e.g., Single Family, Multi Family, Commercial', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='square_footage',
            field=models.IntegerField(default=0, help_text='Total interior square footage of the property'),
        ),
        migrations.AlterField(
            model_name='property',
            name='state',
            field=models.CharField(blank=True, help_text='The state where the property is located', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='year_built',
            field=models.IntegerField(default=0, help_text='The year in which the property was built'),
        ),
        migrations.AlterField(
            model_name='property',
            name='zestimate',
            field=models.DecimalField(decimal_places=2, default=0, help_text="Zillow's estimated market value for the property", max_digits=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='zip_code',
            field=models.CharField(blank=True, help_text='The postal code for the property', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='salesinformation',
            name='deal_strength',
            field=models.CharField(blank=True, help_text='An assessment of the deal strength or likelihood to close successfully', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='salesinformation',
            name='sale_date',
            field=models.DateField(blank=True, help_text='The date on which the sale is completed or expected to be completed', null=True),
        ),
        migrations.AlterField(
            model_name='salesinformation',
            name='sale_status',
            field=models.CharField(blank=True, choices=[('PD', 'Pending'), ('CL', 'Closed')], help_text='The status of the sale, e.g., Pending or Closed', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='salesinformation',
            name='sold_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The amount for which the property was sold', max_digits=12),
        ),
        migrations.AlterField(
            model_name='salesinformation',
            name='stage',
            field=models.CharField(blank=True, choices=[('IN', 'Initial'), ('FU', 'Follow-Up')], help_text='The stage of the sales process, e.g., Initial or Follow-Up', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='taxlien',
            name='certificate_of_release',
            field=models.JSONField(blank=True, help_text='JSON field containing details about the release of the lien, if applicable', null=True),
        ),
        migrations.AlterField(
            model_name='taxlien',
            name='lien_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='The amount of the lien', max_digits=12),
        ),
        migrations.AlterField(
            model_name='taxlien',
            name='lien_date',
            field=models.DateField(blank=True, help_text='The date the tax lien was placed', null=True),
        ),
        migrations.AlterField(
            model_name='taxlien',
            name='lien_type',
            field=models.CharField(blank=True, help_text='The type of tax lien', max_length=100, null=True),
        ),
    ]
