from django.db import models
import os
from tw.settings import *
from PIL import Image

ICON_URL = MEDIA_URL+"icons/"
ICON_EXT = ".png"

def get_extension(path):
    i = path.rfind('.')
    if i == -1:
        return ''
    return path[i+1:]

# Create your models here.

class Researcher(models.Model):
    researcher_name = models.CharField(max_length=25)
    researcher_email = models.CharField(max_length=50)
    researcher_initials = models.CharField(max_length=4)

    def __unicode__(self):
        return self.researcher_initials

class Document(models.Model):
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d', blank=True, null=True)
    document_summary = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.document_name)

class Protocol(models.Model):
    PROTOCOL_CHOICES = (
        ('01', 'Bio Sample Treatment'),
        ('02', 'Experimental Sample'),
        ('03', 'Bio Sample Preparation'),
        ('04', 'Experiment'),
        ('05', 'Subject Organism Treatment'),
        ('06', 'Clinical'),
        ('07', 'Other'),
        ('08', 'Data Processing'),
        ('09', 'Data Transformation'),
        ('10', 'Biomaterial Transformation'),
        ('11', 'Assay'),
    )
    protocol_name = models.CharField(max_length=255)
    protocol_file = models.FileField(upload_to='protocols/%Y/%m/%d', blank=True, null=True)
    protocol_type = models.CharField(max_length=2, choices=PROTOCOL_CHOICES)
    protocol_summary = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.protocol_name)

class Patient(models.Model):
    FAMILY_CHOICES = (
        ('01', 'Father - 01'),
        ('02', 'Mother - 02'),
        ('03', 'Proband - 03'),
        ('33', '2nd Proband - 33'),
        ('04', 'Sibling - 04'),
        ('05', 'Sibling - 05'),
        ('06', 'Sibling - 06'),
        ('99', 'Control - 99'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    YES_NO_CHOICES = (
        ('N', 'No'),
        ('Y', 'Yes'),
    )
    guid = models.CharField(max_length=25)
    family_id = models.CharField(max_length=25)
    family_member = models.CharField(max_length=2, choices=FAMILY_CHOICES)
    biopsy_date = models.DateField(blank=True, null=True)
    age_in_months_at_biopsy = models.IntegerField(blank=True, null=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    race = models.CharField(max_length=255,blank=True, null=True)
    ethnic_group = models.CharField(max_length=255,blank=True, null=True)
    diagnosis = models.CharField(max_length=25, blank=True, null=True)
    head_circumference = models.TextField(blank=True, null=True)
    twin = models.CharField(max_length=1, choices=YES_NO_CHOICES, blank=True, null=True)
    comorbidities = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    patient_file = models.FileField(upload_to='patients/%Y/%m/%d', blank=True, null=True)

    def _get_compound_name(self):
        return u'%s-%s' % (self.family_id, self.family_member)

    compound_name = property(_get_compound_name)

    def __unicode__(self):
        return u'%s-%s' % (self.family_id, self.family_member)

class Vector(models.Model):
    VECTOR_TYPES = (
        ('1', 'iPS Retrovial'),
        ('2', 'iPS Lentiviral'),
        ('3', 'Florescent Neural Differtiation Reporter'),
        ('4', 'Florescent Pluripotency Reporter'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=VECTOR_TYPES)
    sequence = models.TextField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    vector_map = models.TextField(blank=True, null=True)
    researcher = models.ForeignKey(Researcher)
    notes = models.TextField(blank=True, null=True)

class VectorUpload(models.Model):
    Vector_id = models.ForeignKey(Vector, related_name='uploads')
    Vector_image = models.FileField(upload_to='vector_uploads/%Y/%m/%d', blank=True, null=True)
    Vector_file = models.FileField(upload_to='vector_uploads/%Y/%m/%d', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    #def save(self, width=PHOTO_WIDTH, height=PHOTO_HEIGHT, tn_width=PHOTO_THUMBNAIL_WIDTH, tn_height=PHOTO_THUMBNAIL_HEIGHT):
    #    super(VectorUpload, self).save()
    #    if self.Vector_image:
    #        image = Image.open(self.Vector_image.path)
    #        if image.mode not in ('L', 'RGB'):
    #            image = image.convert('RGB')
    #        image.thumbnail((tn_width, tn_height), Image.ANTIALIAS)
    #        filename = self.Vector_image.path
    #        image.save(filename[:filename.rfind(os.sep)+1] + "tmb_" + filename[filename.rfind(os.sep)+1:])
    #        if self.Vector_image.width > width or self.Vector_image.height > height:
    #            filename = self.Vector_image.path
    #            image = Image.open(filename)
    #            image.thumbnail((width, height), Image.ANTIALIAS)
    #            image.save(filename)

    #class Meta:
    #    verbose_name = "Vector Upload"

    #def thumb(self):
    #    if self.Vector_image:
    #        url = self.Vector_image.url
    #        return "<img src='%s' alt='' />" % (url[:url.rfind('/')+1] + "tmb_" + url[url.rfind('/')+1:],)
    #    return ''
    #thumb.allow_tags = True
    #thumb.short_description = 'Image'

    def __unicode__(self):
        return self.Vector_id.name

class Fibroblast(models.Model):
    RACK_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    BOX_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    )
    patient_id = models.ForeignKey(Patient)
    frozen_stock_date = models.DateField()
    passage_number = models.CharField('Passage #',max_length=4)
    researcher = models.ForeignKey(Researcher)
    liq_N2_rack = models.CharField(max_length=1, choices=RACK_CHOICES)
    box_number = models.CharField(max_length=1, choices=BOX_CHOICES)
    vial_location = models.CharField(max_length=25)
    total_vials = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'F%s_P%s' % (self.patient_id, self.passage_number)

class FibroblastBarcode(models.Model):
    Fibroblast_id = models.ForeignKey(Fibroblast)
    barcode = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Fibroblast Barcode"

    def __unicode__(self):
        return self.barcode

class FibroblastUpload(models.Model):
    PF_CHOICES = (
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    )
    Fibroblast_id = models.ForeignKey(Fibroblast, related_name='uploads')
    Fibroblast_SGR_URL = models.CharField(max_length=255, blank=True, null=True)   
    Fibroblast_image = models.ImageField(upload_to='fibroblast_uploads/%Y/%m/%d', blank=True, null=True)
    Fibroblast_file = models.FileField(upload_to='fibroblast_uploads/%Y/%m/%d', blank=True, null=True)
    Fibroblast_pass_fail = models.CharField(max_length=4, choices=PF_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def save(self, width=PHOTO_WIDTH, height=PHOTO_HEIGHT,
             tn_width=PHOTO_THUMBNAIL_WIDTH, tn_height=PHOTO_THUMBNAIL_HEIGHT):
        super(FibroblastUpload, self).save()
        if self.Fibroblast_image:
            image = Image.open(self.Fibroblast_image.path)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            image.thumbnail((tn_width, tn_height), Image.ANTIALIAS)
            filename = self.Fibroblast_image.path
            image.save(filename[:filename.rfind(os.sep)+1] + "tmb_" + filename[filename.rfind(os.sep)+1:])
            #image.save(filename[:filename.rfind('/')+1] + filename[filename.rfind('/')+1:])
            if self.Fibroblast_image.width > width or self.Fibroblast_image.height > height:
                filename = self.Fibroblast_image.path
                image = Image.open(filename)
                image.thumbnail((width, height), Image.ANTIALIAS)
                image.save(filename)
    
    class Meta:
        verbose_name = "Fibroblast Upload"
    
    def thumb(self):
        if self.Fibroblast_image:
            url = self.Fibroblast_image.url
            return "<img src='%s' alt='' />" % (url[:url.rfind('/')+1] + "tmb_" + url[url.rfind('/')+1:],)  
        return ''
    thumb.allow_tags = True 
    thumb.short_description = 'Image'
    
    def __unicode__(self):
        return self.Fibroblast_image.url

class Fibroblast_Sequencing_Prep(models.Model):
    TYPE_CHOICES = (
        ('DNA','DNA'),
        ('RNA','RNA'),
    )
    END_CHOICES = (
        ('1','Single End'),
        ('2','Paired End'),
    )
    PROTOCOL_CHOICES = (
        ('1','Statwd'),
        ('2','Nextera kit Multiplex'),
        ('3','TruSeq kit Multiplex'),
        ('4','Facility Protocol'),
        ('5','Facility Protocol Multiplex'),
        ('6','Facility protocol Ribozero'),
    )
    fibroblast_id = models.ForeignKey(Fibroblast)
    prep_id = models.CharField(max_length=25)
    passage_number = models.CharField('Passage #',max_length=4)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    library_prep_date = models.DateField(blank=True, null=True)
    fragment_size = models.FloatField(blank=True, null=True)
    end = models.CharField(max_length=1, choices=END_CHOICES)
    start_amount = models.FloatField(blank=True, null=True)
    end_amount = models.FloatField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    sequencing_facility = models.CharField(max_length=255)
    protocol = models.CharField(max_length=1, choices=PROTOCOL_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Fibroblast Sequencing Prep"

    def __unicode__(self):
        return u'%s, p%s_%s' % (self.fibroblast_id, self.prep_id, self.type)

class Fibroblast_Flowcell(models.Model):
    fibroblast_sequencing_prep_id = models.ForeignKey(Fibroblast_Sequencing_Prep)
    flowcell_id = models.CharField(max_length=255)
    lane_number = models.IntegerField()
    multiplex = models.CharField(max_length=25, blank=True, null=True)
    URL = models.CharField(max_length=255, blank=True, null=True)
    number_reads = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class Reprogramming(models.Model):
    RACK_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    BOX_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    )
    fibroblast_id = models.ForeignKey(Fibroblast)
    exp_id = models.CharField(max_length=25)
    transfection_date = models.DateField()
    virus_name_prep_date = models.CharField(max_length=25)
    rna_name_prep_date = models.CharField(max_length=25)
    frozen_stock_date = models.DateField(blank=True, null=True)
    researcher = models.ForeignKey(Researcher)
    liq_N2_rack = models.CharField(blank=True, null=True, max_length=1, choices=RACK_CHOICES)
    box_number = models.CharField(blank=True, null=True, max_length=1, choices=BOX_CHOICES)
    vial_location = models.CharField(blank=True, null=True, max_length=25)
    total_vials = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s, R%s' % (self.fibroblast_id, self.transfection_date)

class Ipsc(models.Model):
    RACK_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    BOX_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    )
    transfection_id = models.ForeignKey(Reprogramming)
    ips_clone_id = models.CharField(max_length=25)
    passage_number = models.CharField('Passage #',max_length=4)
    researcher = models.ForeignKey(Researcher)
    frozen_stock_date = models.DateField(blank=True, null=True)
    liq_N2_rack = models.CharField(blank=True, null=True, max_length=1, choices=RACK_CHOICES)
    box_number = models.CharField(blank=True, null=True, max_length=1, choices=BOX_CHOICES)
    vial_location = models.CharField(blank=True, null=True, max_length=25)
    total_vials = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'i%s_P%s, %s' % (self.ips_clone_id, self.passage_number, self.transfection_id)

class iPSCUpload(models.Model):
    UPLOAD_CHOICES = (
        ('',''),
        ('iPSC Image','iPSC Image'),
        ('iPSC RT-PCR','iPSC RT-PCR'),
        ('iPSC Microarray','iPSC Microarray'),
        ('iPSC teratoma','iPSC teratoma'),
    )
    PF_CHOICES = (
        ('In Progress','In Progress'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    )
    iPSC_id = models.ForeignKey(Ipsc, related_name='uploads')
    iPSC_upload_type = models.CharField(max_length=20, choices=UPLOAD_CHOICES)
    iPSC_sample_image = models.ImageField(upload_to='ipsc_uploads/%Y/%m/%d', blank=True, null=True)
    iPSC_control_image = models.ImageField(upload_to='ipsc_uploads/%Y/%m/%d', blank=True, null=True)
    iPSC_file = models.FileField(upload_to='ipsc_uploads/%Y/%m/%d', blank=True, null=True)
    iPSC_pass_fail = models.CharField(max_length=11, choices=PF_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    #def status(self):
        #if self.iPSC_pass_fail:
            #mystatus = self.iPSC_pass_fail
            #return mystatus
        #return ''
    #status.allow_tags = True
    #status.short_description = 'Status'

    def __unicode__(self):
        return self.iPSC_upload_type

class iPSCBarcode(models.Model):
    iPSC_id = models.ForeignKey(Ipsc)
    barcode = models.CharField(max_length=255)

    class Meta:
        verbose_name = "iPSC Barcode"

    def __unicode__(self):
        return self.barcode

class Ipsc_Sequencing_Prep(models.Model):
    TYPE_CHOICES = (
        ('DNA','DNA'),
        ('RNA','RNA'),
    )
    END_CHOICES = (
        ('1','Single End'),
        ('2','Paired End'),
    )
    PROTOCOL_CHOICES = (
        ('1','Statwd'),
        ('2','Nextera kit Multiplex'),
        ('3','TruSeq kit Multiplex'),
        ('4','Facility Protocol'),
        ('5','Facility Protocol Multiplex'),
        ('6','Facility protocol Ribozero'),
    )
    ipsc_id = models.ForeignKey(Ipsc)
    prep_id = models.CharField(max_length=25)
    dna_passage_number = models.CharField('DNA P #',max_length=4,blank=True, null=True)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    library_prep_date = models.DateField(blank=True, null=True)
    fragment_size = models.FloatField(blank=True, null=True)
    end = models.CharField(max_length=1, choices=END_CHOICES)
    start_amount = models.FloatField(blank=True, null=True)
    end_amount = models.FloatField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    sequencing_facility = models.CharField(max_length=255)
    protocol = models.CharField(max_length=1, choices=PROTOCOL_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "iPSC Sequencing Prep"

    def __unicode__(self):
        return u'%s, p%s_%s' % (self.ipsc_id, self.prep_id, self.type)

class Ipsc_Flowcell(models.Model):
    ipsc_sequencing_prep_id = models.ForeignKey(Ipsc_Sequencing_Prep)
    flowcell_id = models.CharField(max_length=255)
    lane_number = models.IntegerField()
    multiplex = models.CharField(max_length=25, blank=True, null=True)
    URL = models.CharField(max_length=255, blank=True, null=True)
    number_reads = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class Neuronal_Progenitor(models.Model):
    RACK_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    BOX_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    )
    iPSC_id = models.ForeignKey(Ipsc)
    np_id = models.CharField(max_length=25)
    differentiation_start_date = models.DateField()
    protocol = models.ForeignKey(Protocol)
    num_days_in_culture = models.IntegerField()
    frozen_stock_date = models.DateField(blank=True, null=True)
    researcher = models.ForeignKey(Researcher)
    liq_N2_rack = models.CharField(blank=True, null=True, max_length=1, choices=RACK_CHOICES)
    box_number = models.CharField(blank=True, null=True, max_length=1, choices=BOX_CHOICES)
    vial_location = models.CharField(blank=True, null=True, max_length=25)
    total_vials = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def thumb(self):
        for upload in self.np_uploads.all():
            if upload.np_image:
                url = upload.np_image.url
                return "<img src='%s' alt='' />" % (url[:url.rfind('/')+1] + "tmb_" + url[url.rfind('/')+1:],)
        return ''
    thumb.allow_tags = True
    thumb.short_description = 'Image'

    class Meta:
        verbose_name = "Neuronal Progenitor"

    def __unicode__(self):
        return u'NP%s, %s' % (self.np_id, self.iPSC_id)

class NPBarcode(models.Model):
    np_id = models.ForeignKey(Neuronal_Progenitor)
    barcode = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Neuronal Progenitor Barcode"

    def __unicode__(self):
        return self.barcode

class NPUpload(models.Model):
    UPLOAD_CHOICES = (
        ('Cell Differentiation','Cell Differentiation'),
        ('Cell Proliferation','Cell Proliferation'),
        ('Cell Survival','Cell Survival'),
        ('Neuron Counts','Neuron Counts'),
        ('Neuron Images','Neuron Images'),
    )
    np_id = models.ForeignKey(Neuronal_Progenitor, related_name='np_uploads')
    np_upload_type = models.CharField(max_length=20, choices=UPLOAD_CHOICES, blank=True, null=True)
    np_image = models.ImageField(upload_to='np_uploads/%Y/%m/%d', blank=True, null=True)
    np_file = models.FileField(upload_to='np_uploads/%Y/%m/%d', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def save(self, width=PHOTO_WIDTH, height=PHOTO_HEIGHT,
             tn_width=PHOTO_THUMBNAIL_WIDTH, tn_height=PHOTO_THUMBNAIL_HEIGHT):
        super(NPUpload, self).save()
        if self.np_image:
            image = Image.open(self.np_image.path)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            image.thumbnail((tn_width, tn_height), Image.ANTIALIAS)
            filename = self.np_image.path
            image.save(filename[:filename.rfind(os.sep)+1] + "tmb_" + filename[filename.rfind(os.sep)+1:])
            if self.np_image.width > width or self.np_image.height > height:
                filename = self.np_image.path
                image = Image.open(filename)
                image.thumbnail((width, height), Image.ANTIALIAS)
                image.save(filename)

    class Meta:
        verbose_name = "Neuronal Progenitor Upload"

    def thumb(self):
        if self.np_image:
            url = self.np_image.url
            return "<img src='%s' alt='' />" % (url[:url.rfind('/')+1] + "tmb_" + url[url.rfind('/')
+1:],)
        return ''
    thumb.allow_tags = True
    thumb.short_description = 'Image'

    def __unicode__(self):
        return self.np_upload_type

class Neuronal_Progenitor_Sequencing_Prep(models.Model):
    TYPE_CHOICES = (
        ('DNA','DNA'),
        ('RNA','RNA'),
    )
    END_CHOICES = (
        ('1','Single End'),
        ('2','Paired End'),
    )
    PROTOCOL_CHOICES = (
        ('1','Statwd'),
        ('2','Nextera kit Multiplex'),
        ('3','TruSeq kit Multiplex'),
        ('4','Facility Protocol'),
        ('5','Facility Protocol Multiplex'),
        ('6','Facility protocol Ribozero'),
    )
    np_id = models.ForeignKey(Neuronal_Progenitor)
    prep_id = models.CharField(max_length=25)
    passage_number = models.CharField('Passage #',max_length=4)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    library_prep_date = models.DateField(blank=True, null=True)
    fragment_size = models.FloatField(blank=True, null=True)
    end = models.CharField(max_length=1, choices=END_CHOICES)
    start_amount = models.FloatField(blank=True, null=True)
    end_amount = models.FloatField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    sequencing_facility = models.CharField(max_length=255)
    protocol = models.CharField(max_length=1, choices=PROTOCOL_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Neuronal Progenitor Sequencing Prep"

    def __unicode__(self):
        return u'%s, p%s_%s' % (self.np_id, self.prep_id, self.type)

class Neuronal_Progenitor_Flowcell(models.Model):
    np_sequencing_prep_id = models.ForeignKey(Neuronal_Progenitor_Sequencing_Prep)
    flowcell_id = models.CharField(max_length=255)
    lane_number = models.IntegerField()
    multiplex = models.CharField(max_length=25, blank=True, null=True)
    URL = models.CharField(max_length=255, blank=True, null=True)
    number_reads = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
