from tw.lims.models import *
from django.contrib import admin
from tw.lims.widgets import *

class ResearcherAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['researcher_name', 'researcher_email', 'researcher_initials']
    search_fields = ['researcher_name', 'researcher_email', 'researcher_initials']

class DocumentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['document_name','document_file','document_summary']
    search_fields = ['document_name']

class ProtocolAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['protocol_name','protocol_file','protocol_type','protocol_summary']
    search_fields = ['protocol_name']

class PatientAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['guid','family_id','family_member','gender','race','ethnic_group','biopsy_date','year_of_birth','age_in_months_at_biopsy','diagnosis','head_circumference','twin']
    search_fields = ['guid','family_id','year_of_birth','diagnosis','notes']
    list_filter = ['family_id','family_member','biopsy_date']

class VectorUploadInline(admin.TabularInline):
    save_on_top = True
    model = VectorUpload
    extra = 1

    #def formfield_for_dbfield(self, db_field, **kwargs):
        #if db_field.name == 'Vector_image':
            #kwargs['widget'] = AdminImageWidget
        #return super(VectorUploadInline,self).formfield_for_dbfield(db_field,**kwargs)

class VectorAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [VectorUploadInline]
    list_display = ['name','type','researcher']

class FibroblastUploadInline(admin.TabularInline):
    save_on_top = True
    model = FibroblastUpload
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'Fibroblast_image':
            kwargs['widget'] = AdminImageWidget
        return super(FibroblastUploadInline,self).formfield_for_dbfield(db_field,**kwargs)

class FibroblastBarcodeAdmin(admin.ModelAdmin):
    save_on_top = True
    raw_id_fields = ('Fibroblast_id',)
    list_display = ['barcode','Fibroblast_id']
    search_fields = ['barcode','Fibroblast_id__patient_id__family_id','Fibroblast_id__patient_id__family_member']

class FibroblastBarcodeInline(admin.TabularInline):
    save_on_top = True
    model = FibroblastBarcode
    extra = 10

class FibroblastAdmin(admin.ModelAdmin):
    save_on_top = True
    
    def pass_or_fail(self,obj):
        retval = ''
        fibuploads = obj.fibroblast_upload_set.all()
        if len(fibuploads) > 0:
            retval = 'Fail'
            for fibupload in fibuploads:
                if fibupload.Fibroblast_pass_fail == 'Pass':
                    retval = 'Pass'
        
        return retval
    
    inlines = [FibroblastBarcodeInline, FibroblastUploadInline]
    raw_id_fields = ('patient_id',)
    list_display = ['patient_id','frozen_stock_date','passage_number','researcher','liq_N2_rack','box_number','vial_location','total_vials','pass_or_fail']
    search_fields = ['patient_id__family_id','patient_id__family_member','passage_number','notes']
    list_filter = ['patient_id__family_id','patient_id__family_member']

class FibroblastFlowcellInline(admin.TabularInline):
    save_on_top = True
    model = Fibroblast_Flowcell
    extra = 1

class FibroblastSequencingPrepAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [FibroblastFlowcellInline]
    list_display = ['fibroblast_id','prep_id','type','library_prep_date','fragment_size','end','start_amount','end_amount','submission_date','sequencing_facility','protocol']
    search_fields = ['fibroblast_id__patient_id__family_id','fibroblast_id__patient_id__family_member','notes']
    list_filter = ['fibroblast_id__patient_id__family_id','fibroblast_id__patient_id__family_member','type']    

class ReprogrammingAdmin(admin.ModelAdmin):
    save_on_top = True
    raw_id_fields = ('fibroblast_id',)
    list_display = ['fibroblast_id','exp_id','transfection_date','virus_name_prep_date','rna_name_prep_date','frozen_stock_date','researcher','liq_N2_rack','box_number','vial_location','total_vials']
    search_fields = ['fibroblast_id__patient_id__family_id','fibroblast_id__patient_id__family_member','fibroblast_id__passage_number','ipsc_id','notes']
    list_filter = ['fibroblast_id__patient_id__family_id','fibroblast_id__patient_id__family_member']    

class iPSCUploadInline(admin.TabularInline):
    save_on_top = True
    model = iPSCUpload
    extra = 1

    #def formfield_for_dbfield(self, db_field, **kwargs):
        #if db_field.name == 'iPSC_pass_fail':
            #kwargs['widget'] = AdminStatusWidget
        #return super(iPSCUploadInline,self).formfield_for_dbfield(db_field, **kwargs)

class iPSCBarcodeInline(admin.TabularInline):
    save_on_top = True
    model = iPSCBarcode
    extra = 1

class iPSCBarcodeAdmin(admin.ModelAdmin):
    save_on_top = True
    raw_id_fields = ('iPSC_id',)
    list_display = ['barcode','iPSC_id']
    search_fields = ['barcode','iPSC_id__transfection_id__fibroblast_id__patient_id__family_id','iPSC_id__transfection_id__fibroblast_id__patient_id__family_member']

class IpscAdmin(admin.ModelAdmin):
    save_on_top = True
    def qc(self,obj,type):
        retvals = ['Pass','In Progress','Fail',None]
        i = j = retvals.index(None)
        qcs = obj.uploads.filter(iPSC_upload_type = type);
        for qc in qcs:
            j = retvals.index(qc.iPSC_pass_fail)
            if j < i: i = j
        return retvals[j]
        
    def image_qc(self,obj):
        return self.qc(obj,'iPSC Image')
    
    def rt_pcr_qc(self,obj):
        return self.qc(obj,'iPSC RT-PCR')
    
    def microarray_qc(self,obj):
        return self.qc(obj,'iPSC Microarray')
    
    def final_qc(self,obj):
        i = self.image_qc(obj)
        r = self.rt_pcr_qc(obj)
        m = self.microarray_qc(obj)
        
        if i == None or r == None or m == None:
            return None
        
        if i == 'In Progress' or r == 'In Progress' or m == 'In Progress': 
            return 'In Progress'
        
        if i == 'Pass' and r == 'Pass' and m == 'Pass':
            return 'Pass'
        
        return 'Fail'
    
    image_qc.short_description = 'Image QC'
    rt_pcr_qc.short_description = 'RT-PCR QC'
    microarray_qc.short_description = 'Microarray QC'
    final_qc.short_description = 'Final QC'
    
    inlines = [iPSCBarcodeInline, iPSCUploadInline]
    raw_id_fields = ('transfection_id',)
    list_display = ['transfection_id','ips_clone_id','passage_number','researcher','liq_N2_rack','box_number','vial_location','total_vials','image_qc','rt_pcr_qc','microarray_qc','final_qc']
    list_display_links = ['transfection_id','ips_clone_id']
    search_fields = ['transfection_id__fibroblast_id__patient_id__family_id','transfection_id__fibroblast_id__patient_id__family_member','transfection_id__fibroblast_id__passage_number','passage_number','notes']
    list_filter = ['transfection_id__fibroblast_id__patient_id__family_id','transfection_id__fibroblast_id__patient_id__family_member']

class IpscFlowcellInline(admin.TabularInline):
    save_on_top = True
    model = Ipsc_Flowcell
    extra = 1

class IpscSequencingPrepAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [IpscFlowcellInline]
    raw_id_fields = ('ipsc_id',)
    list_display = ['ipsc_id','prep_id','type','dna_passage_number','library_prep_date','fragment_size','end','start_amount','end_amount','submission_date','sequencing_facility','protocol']
    search_fields = ['ipsc_id__transfection_id__fibroblast_id__patient_id__family_id','ipsc_id__transfection_id__fibroblast_id__patient_id__family_member','notes']
    list_filter = ['ipsc_id__transfection_id__fibroblast_id__patient_id__family_id','ipsc_id__transfection_id__fibroblast_id__patient_id__family_member','type']

class NPUploadInline(admin.TabularInline):
    save_on_top = True
    model = NPUpload
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'np_image':
            kwargs['widget'] = AdminImageWidget
        return super(NPUploadInline,self).formfield_for_dbfield(db_field,**kwargs)

class NPBarcodeInline(admin.TabularInline):
    save_on_top = True
    model = NPBarcode
    extra = 1

class Neuronal_ProgenitorAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [NPBarcodeInline, NPUploadInline]
    raw_id_fields = ('iPSC_id',)
    list_display = ['iPSC_id','np_id','differentiation_start_date','protocol','num_days_in_culture','frozen_stock_date','researcher','liq_N2_rack','box_number','vial_location','total_vials','thumb']
    search_fields = ['iPSC_id__transfection_id__fibroblast_id__patient_id__guid','iPSC_id__transfection_id__fibroblast_id__patient_id__family_id','iPSC_id__transfection_id__fibroblast_id__passage_number','iPSC_id__passage_number','notes']
    list_filter = ['iPSC_id__transfection_id__fibroblast_id__patient_id__family_id','iPSC_id__transfection_id__fibroblast_id__patient_id__family_member']

class NeuronalProgenitorFlowcellInline(admin.TabularInline):
    save_on_top = True
    model = Neuronal_Progenitor_Flowcell
    extra = 1

class NeuronalProgenitorSequencingPrepAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [NeuronalProgenitorFlowcellInline]
    raw_id_fields = ('np_id',)
    list_display = ['np_id','prep_id','type','library_prep_date','fragment_size','end','start_amount','end_amount','submission_date','sequencing_facility','protocol']
    search_fields = ['np_id__iPSC_id__transfection_id__fibroblast_id__patient_id__family_id','np_id__iPSC_id__transfection_id__fibroblast_id__patient_id__family_member','notes']
    list_filter = ['np_id__iPSC_id__transfection_id__fibroblast_id__patient_id__family_id','np_id__iPSC_id__transfection_id__fibroblast_id__patient_id__family_member','type']


admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Vector, VectorAdmin)
admin.site.register(Fibroblast, FibroblastAdmin)
admin.site.register(FibroblastBarcode, FibroblastBarcodeAdmin)
admin.site.register(Fibroblast_Sequencing_Prep, FibroblastSequencingPrepAdmin)
admin.site.register(Reprogramming, ReprogrammingAdmin)
admin.site.register(Ipsc, IpscAdmin)
admin.site.register(iPSCBarcode, iPSCBarcodeAdmin)
admin.site.register(Ipsc_Sequencing_Prep, IpscSequencingPrepAdmin)
admin.site.register(Neuronal_Progenitor, Neuronal_ProgenitorAdmin)
admin.site.register(Neuronal_Progenitor_Sequencing_Prep, NeuronalProgenitorSequencingPrepAdmin)
