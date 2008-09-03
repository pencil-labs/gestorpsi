# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.place.models import PlaceType, Place
from gestorpsi.address.models import City, State, Country, AddressType
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from django.contrib import admin
import unittest
from django.test.client import Client

class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.place= Place(label='testing place', visible= True )
        place_type= PlaceType(description= 'a place type')
        place_type.save()
        self.place.place_type= place_type
        phone_type= PhoneType(description= 'phone type test')
        phone= Phone(area= '23', phoneNumber= '45679078', ext= '4444', phoneType= phone_type)
        phone.content_object = self.place

        addressType=AddressType(description='Home')
        addressType.save()
        address = Address()
        address.addressPrefix = 'Rua'
        address.addressLine1 = 'Rui Barbosa, 1234'
        address.addressLine2 = 'Anexo II - Sala 4'
        address.neighborhood = 'Centro'
        address.zipCode = '12345-123'
        address.addressType = AddressType.objects.get(pk=1)

        country= Country( name= 'test', nationality= 'testing' )
        country.save()
        state= State(name= 'test', shortName= 't', country= country )
        state.save()
        city= City(name= 'test', state= state)
        city.save()

        address.city = city
        address.content_object = self.place

        self.place.save()

    def testDefaultPlace(self):
        #get all places stored in the database and put them in a list
        #then compare the first (and probably only) stored-place with self.place 
        self.assertEquals(  Place.objects.all()[0], self.place, 'place has not been appropriately saved' )

class ViewPlaceTest( unittest.TestCase ):
    urls = 'gestorpsi.place.urls'
    
    def setUp(self):
        print 'setup'
        
    def testIndex(self):
        #c= Client()
        #print "%s" % c.post( '/index/', { 'joaoajoa': 2 } )
        #self.assertEquals( 200, response.status_code )
        pass

    def tearDown(self):
        print 'teardown'
       
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase( PlaceTest )
    suite.addTest( ViewPlaceTest('testIndex'))
    return suite