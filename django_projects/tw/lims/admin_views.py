from tw.lims.models import Patient
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

cmpkey = 0
attrs = ['link','parent_id','prep_id','type','fragment_size','end','submission_date','sequencing_facility','flowcell_id','lane_number']

def test(request):
    from django.db import connection
    cursor = connection.cursor()
#    query_string = ("""
#        SELECT
#            distinct family_id, family_member, ips_clone_id, type, end, submission_date, sequencing_facility, flowcell_id, lane_number
#        FROM
#            lims_patient 
#        JOIN
#            lims_fibroblast 
#        ON 
#            lims_patient.id = lims_fibroblast.patient_id_id
#        JOIN
#            lims_reprogramming 
#        ON 
#            lims_fibroblast.id = lims_reprogramming.fibroblast_id_id
#        JOIN
#            lims_ipsc 
#        ON 
#            lims_reprogramming.id = lims_ipsc.transfection_id_id
#        LEFT OUTER JOIN
#            lims_ipsc_sequencing_prep 
#        ON 
#            lims_ipsc.id = lims_ipsc_sequencing_prep.ipsc_id_id
#        LEFT OUTER JOIN
#            lims_ipsc_flowcell 
#        ON 
#            lims_ipsc_sequencing_prep.id = lims_ipsc_flowcell.ipsc_sequencing_prep_id_id
#        WHERE
#            lims_patient.family_id = '03'
#        ORDER BY
#            family_id, family_member, ips_clone_id, type, end
#    """)

    query_string = ("""
        SELECT
            distinct family_id, family_member, ips_clone_id
        FROM
            lims_patient 
        JOIN
            lims_fibroblast 
        ON 
            lims_patient.id = lims_fibroblast.patient_id_id
        JOIN
            lims_reprogramming 
        ON 
            lims_fibroblast.id = lims_reprogramming.fibroblast_id_id
        JOIN
            lims_ipsc 
        ON 
            lims_reprogramming.id = lims_ipsc.transfection_id_id
        ORDER BY
            family_id, family_member, ips_clone_id
    """)
    cursor.execute(query_string)
    results = cursor.fetchall()
    return render_to_response('admin/ipsc.html',{'results': results},RequestContext(request, {}),)
    test = staff_member_required(test)

def ipsc(request):
    from operator import attrgetter

    patient_id = int(request.GET.get('patientid',0))
    family_id = request.GET.get('familyid','0')
    family_ids = []
    patients = Patient.objects.all().order_by('family_id')
    for p in patients:
        if p.family_id not in family_ids:
            family_ids += [p.family_id]
    include = request.GET.getlist('include')
    cmpkey = int(request.GET.get('o',0))
    order = request.GET.get('ot','asc')
    ipscs = []
    if family_id != '0':
        ipscs = family_ipsc(family_id,include)
    else:
        ipscs = patient_ipsc(patient_id,include)

    ipscs.sort(key=attrgetter(attrs[cmpkey]),cmp=fccmp,reverse=(order=='desc'))

    url = request.get_full_path()
    if url.count('&o=') > 0:
        url = url[0:url.index('&o=')]
    if url.count('&ot=') > 0:
        url = url[0:url.index('&ot=')]

    return render_to_response(
        "admin/ipsc.html",
        {'patient_list' : Patient.objects.all().order_by('family_id'),
        'patientid':patient_id,
        'family_ids':family_ids,
        'familyid':family_id,
        'include':include,
        'ipscs':ipscs,
        'url':url,
        'sort':cmpkey,
        'order':order},
        RequestContext(request, {}),
    )

def report(request):
    
    patient_id = int(request.GET.get('patientid',0))
    family_id = request.GET.get('familyid','0')
    family_ids = []
    patients = Patient.objects.all()
    for p in patients:
        if p.family_id not in family_ids:
            family_ids += [p.family_id]
    
    include = request.GET.getlist('include')
    images = []
    if family_id != '0':
        images = family_image(family_id,include)
    else:
        images = patient_image(patient_id,include)
    url = "/admin/lims/patient/"
    if patient_id:
        url += str(patient_id) + '/'
    no_image = True
    if len(images) > 0:
        no_image = False

    return render_to_response(
        "admin/report.html",
        {'patient_list' : patients,
        'patientid':patient_id,
        'family_ids':family_ids,
        'familyid':family_id,
        'include':include,
        'url':url,
        'images':images,
        'no_image':no_image},
        RequestContext(request, {}),
    )

def flowcell(request):
    from operator import attrgetter
    
    patient_id = int(request.GET.get('patientid',0))
    family_id = request.GET.get('familyid','0')
    family_ids = []
    patients = Patient.objects.all().order_by('family_id')
    for p in patients:
        if p.family_id not in family_ids:
            family_ids += [p.family_id]
    include = request.GET.getlist('include')
    cmpkey = int(request.GET.get('o',0))
    order = request.GET.get('ot','asc')
    flowcells = []
    if family_id != '0':
        flowcells = family_flowcell(family_id,include)
    else:
        flowcells = patient_flowcell(patient_id,include)
    
    flowcells.sort(key=attrgetter(attrs[cmpkey]),cmp=fccmp,reverse=(order=='desc'))
    
    url = request.get_full_path()
    if url.count('&o=') > 0:
        url = url[0:url.index('&o=')]
    if url.count('&ot=') > 0:
        url = url[0:url.index('&ot=')]

    return render_to_response(
        "admin/flowcell.html",
        {'patient_list' : Patient.objects.all().order_by('family_id'),
        'patientid':patient_id,
        'family_ids':family_ids,
        'familyid':family_id,
        'include':include,
        'flowcells':flowcells,
        'url':url,
        'sort':cmpkey,
        'order':order},
        RequestContext(request, {}),
    )
    
flowcell = staff_member_required(flowcell)
ipsc = staff_member_required(ipsc)
report = staff_member_required(report)

def family_image(family_id,include):
    patients = Patient.objects.filter(family_id=family_id)
    images = []
    for patient in patients:
        images += patient_image(patient.id,include)
    return images

def patient_image(patient_id,include):
    images = []
    if patient_id == 0:
        return images
    patient = Patient.objects.get(id=patient_id)
    
    fibroblasts = patient.fibroblast_set.all()
    for fibroblast in fibroblasts:
        if u'fb' in include:
            for fbupload in fibroblast.uploads.all():
                image = Image(fbupload.Fibroblast_image.url,"/admin/lims/fibroblast/%d/" % fibroblast.id,fibroblast)
                images.append(image)
            
        for reprogramming in fibroblast.reprogramming_set.all():
            for ipsc in reprogramming.ipsc_set.all():
                
                if u'ips' in include:
                    for ipscupload in ipsc.uploads.all():
                        image = Image('',"/admin/lims/ipsc/%d/" % ipsc.id,ipsc)
                        if ipscupload.iPSC_sample_image:
                            image.url = ipscupload.iPSC_sample_image.url
                        if ipscupload.iPSC_control_image:
                            image.control_url = ipscupload.iPSC_control_image.url
                        images.append(image)
                    
                if u'np' in include:
                    for np in ipsc.neuronal_progenitor_set.all():
                        for npupload in np.np_uploads.all():
                            image = Image(npupload.np_image.url,"/admin/lims/neuronal_progenitor/%d/" % np.id,np)
                            images.append(image)
            
    return images

def family_ipsc(family_id,include):
    patients = Patient.objects.filter(family_id=family_id)
    ipscs = []
    for patient in patients:
        ipscs += patient_ipsc(patient.id,include)
    return ipscs

def patient_ipsc(patient_id,include):
    ipscs = []
    
    patients = []
    if patient_id == 0:
        patients = Patient.objects.all()
    else:
        patients.append(Patient.objects.get(id=patient_id))
    
    for patient in patients:
        fibroblasts = patient.fibroblast_set.all()
        for fibroblast in fibroblasts:
            for reprogramming in fibroblast.reprogramming_set.all():
                #for ips in reprogramming.ipsc_set.distinct('ips_clone_id'):
                for ips in reprogramming.ipsc_set.all():
#                    for prep in ips.ipsc_sequencing_prep_set.all():
#                        fcs = prep.ipsc_flowcell_set.all()
#                        if len(fcs) > 0:
#                            for fc in fcs:
#                                ipsc = Ipsc(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ips.ips_clone_id),
#                                                    '/admin/lims/ipsc/%d/' % ips.id,
#                                                    prep.end, prep.submission_date,
#                                                    prep.sequencing_facility,
#                                                    fc.flowcell_id,fc.lane_number )
#                        else:
#                            ipsc = Ipsc(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ips.ips_clone_id),
#                                                '/admin/lims/ipsc/%d/' % ips.id,
#                                                prep.end, prep.submission_date,
#                                                prep.sequencing_facility,
#                                                'None','None')
                    ipsc = Ipsc(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ips.ips_clone_id),
                                        '/admin/lims/ipsc/%d/' % ips.id )
                    ipscs.append(ipsc)
    return ipscs
    
def family_flowcell(family_id,include):
    patients = Patient.objects.filter(family_id=family_id)
    flowcells = []
    for patient in patients:
        flowcells += patient_flowcell(patient.id,include)
    return flowcells

def patient_flowcell(patient_id,include):
    flowcells = []
    
    patients = []
    if patient_id == 0:
        patients = Patient.objects.all()
    else:
        patients.append(Patient.objects.get(id=patient_id))
    
    for patient in patients:
        fibroblasts = patient.fibroblast_set.all()
        for fibroblast in fibroblasts:
            if u'fb' in include:
                for prep in fibroblast.fibroblast_sequencing_prep_set.all():
                    if u'dna' in include and prep.type == 'DNA':
                        fcs = prep.fibroblast_flowcell_set.all()
                        if len(fcs) > 0:
                            for fc in fcs:
                                flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                    '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                    prep.prep_id,prep.type,prep.fragment_size,
                                                    prep.end, prep.submission_date,
                                                    prep.sequencing_facility,
                                                    fc.flowcell_id,fc.lane_number)
                                
                                flowcells.append(flowcell)
                        else:
                            flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                prep.prep_id,prep.type,prep.fragment_size,
                                                prep.end, prep.submission_date,
                                                prep.sequencing_facility,
                                                'None','None')
                            
                            flowcells.append(flowcell)
                    elif u'rna' in include and prep.type == 'RNA':
                        fcs = prep.fibroblast_flowcell_set.all()
                        if len(fcs) > 0:
                            for fc in fcs:
                                flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                    '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                    prep.prep_id,prep.type,prep.fragment_size,
                                                    prep.end, prep.submission_date,
                                                    prep.sequencing_facility,
                                                    fc.flowcell_id,fc.lane_number)
                                
                                flowcells.append(flowcell)
                        else:
                            flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                prep.prep_id,prep.type,prep.fragment_size,
                                                prep.end, prep.submission_date,
                                                prep.sequencing_facility,
                                                'None','None')
                            
                            flowcells.append(flowcell)
                    elif u'rna' not in include and u'dna' not in include:
                        fcs = prep.fibroblast_flowcell_set.all()
                        if len(fcs) > 0:
                            for fc in fcs:
                                flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                    '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                    prep.prep_id,prep.type,prep.fragment_size,
                                                    prep.end, prep.submission_date,
                                                    prep.sequencing_facility,
                                                    fc.flowcell_id,fc.lane_number)
                                
                                flowcells.append(flowcell)
                        else:
                            flowcell = Flowcell(u'F%s_P%s' % (fibroblast.patient_id, fibroblast.passage_number),
                                                '/admin/lims/fibroblast_sequencing_prep/%d/' % prep.id,
                                                prep.prep_id,prep.type,prep.fragment_size,
                                                prep.end, prep.submission_date,
                                                prep.sequencing_facility,
                                                'None','None')
                            
                            flowcells.append(flowcell)
                        
                
            for reprogramming in fibroblast.reprogramming_set.all():
                for ipsc in reprogramming.ipsc_set.all():
                    
                    if u'ips' in include:
                        for prep in ipsc.ipsc_sequencing_prep_set.all():
                            if u'dna' in include and prep.type == 'DNA':
                                fcs = prep.ipsc_flowcell_set.all()
                                if len(fcs) > 0:
                                    for fc in fcs:
                                        flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                        #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                            '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            fc.flowcell_id,fc.lane_number )
                                        
                                        flowcells.append(flowcell)
                                else:
                                    flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                    #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                        '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                        prep.prep_id,prep.type,prep.fragment_size,
                                                        prep.end, prep.submission_date,
                                                        prep.sequencing_facility,
                                                        'None','None')
                                    
                                    flowcells.append(flowcell)
                            elif u'rna' in include and prep.type == 'RNA':
                                fcs = prep.ipsc_flowcell_set.all()
                                if len(fcs) > 0:
                                    for fc in fcs:
                                        flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                        #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                            '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            fc.flowcell_id,fc.lane_number )
                                        
                                        flowcells.append(flowcell)
                                else:
                                    flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                    #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                        '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                        prep.prep_id,prep.type,prep.fragment_size,
                                                        prep.end, prep.submission_date,
                                                        prep.sequencing_facility,
                                                        'None','None')
                                    
                                    flowcells.append(flowcell)
                            elif u'dna' not in include and u'rna' not in include:
                                fcs = prep.ipsc_flowcell_set.all()
                                if len(fcs) > 0:
                                    for fc in fcs:
                                        flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                        #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                            '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            fc.flowcell_id,fc.lane_number )
                                        
                                        flowcells.append(flowcell)
                                else:
                                    flowcell = Flowcell(u'i%s-%s #%s' % (patient.family_id, patient.family_member, ipsc.ips_clone_id),
                                    #flowcell = Flowcell(u'i%s_P%s_%s' % (ipsc.ips_clone_id, ipsc.passage_number, ipsc.transfection_id),
                                                        '/admin/lims/ipsc_sequencing_prep/%d/' % prep.id,
                                                        prep.prep_id,prep.type,prep.fragment_size,
                                                        prep.end, prep.submission_date,
                                                        prep.sequencing_facility,
                                                        'None','None')
                                    
                                    flowcells.append(flowcell)
                        
                    if u'np' in include:
                        for np in ipsc.neuronal_progenitor_set.all():
                            for prep in np.neuronal_progenitor_sequencing_prep_set.all():
                                if u'dna' in include and prep.type == 'DNA':
                                    fcs = prep.neuronal_progenitor_flowcell_set.all()
                                    if len(fcs) > 0:
                                        for fc in fcs:
                                            flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                                '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                                prep.prep_id,prep.type,prep.fragment_size,
                                                                prep.end, prep.submission_date,
                                                                prep.sequencing_facility,
                                                                fc.flowcell_id,fc.lane_number )
                                            
                                            flowcells.append(flowcell)
                                    else:
                                        flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                            '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            'None','None')
                                        
                                        flowcells.append(flowcell)
                                elif u'rna' in include and prep.type == 'RNA':
                                    fcs = prep.neuronal_progenitor_flowcell_set.all()
                                    if len(fcs) > 0:
                                        for fc in fcs:
                                            flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                                '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                                prep.prep_id,prep.type,prep.fragment_size,
                                                                prep.end, prep.submission_date,
                                                                prep.sequencing_facility,
                                                                fc.flowcell_id,fc.lane_number )
                                            
                                            flowcells.append(flowcell)
                                    else:
                                        flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                            '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            'None','None')
                                        
                                        flowcells.append(flowcell)
                                elif u'dna' not in include and u'rna' not in include:
                                    fcs = prep.neuronal_progenitor_flowcell_set.all()
                                    if len(fcs) > 0:
                                        for fc in fcs:
                                            flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                                '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                                prep.prep_id,prep.type,prep.fragment_size,
                                                                prep.end, prep.submission_date,
                                                                prep.sequencing_facility,
                                                                fc.flowcell_id,fc.lane_number )
                                            
                                            flowcells.append(flowcell)
                                    else:
                                        flowcell = Flowcell(u'NP%s, %s' % (np.np_id, np.iPSC_id),
                                                            '/admin/lims/neuronal_progenitor_sequencing_prep/%d/' % prep.id,
                                                            prep.prep_id,prep.type,prep.fragment_size,
                                                            prep.end, prep.submission_date,
                                                            prep.sequencing_facility,
                                                            'None','None')
                                        
                                        flowcells.append(flowcell)
            
    return flowcells

class Image:
    url = ''
    control_url = ''
    link = ''
    title = ''
    
    def __init__(self,u,l,t):
        self.url = u
        self.link = l
        self.title = t
    
class Ipsc:
    parent_id = ''
    link = ''
#    end = ''
#    submission_date  = ''
#    sequencing_facility  = ''
#    flowcell_id  = ''
#    lane_number  = ''

    def __init__(self,pid,l):
#    def __init__(self,pid,l,e,sd,sf,fid,fln):
        self.parent_id = pid
        self.link = l
#        self.end = e
#        self.submission_date = sd
#        self.sequencing_facility  = sf
#        self.flowcell_id  = fid
#        self.lane_number  = fln

class Flowcell:
    parent_id = ''
    link = ''
    prep_id = ''
    type = ''
    fragment_size = ''
    end = ''
    submission_date  = ''
    sequencing_facility  = ''
    flowcell_id  = ''
    lane_number  = ''
    
    def __init__(self,pid,l,prepid,t,fs,e,sd,sf,fid,fln):
        self.parent_id = pid
        self.link = l
        self.prep_id = prepid
        self.type = t
        self.fragment_size = fs
        self.end = e
        self.submission_date = sd
        self.sequencing_facility  = sf
        self.flowcell_id  = fid
        self.lane_number  = fln
        
def fccmp(x,y):
    if not x:
        return -1
    if not y:
        return 1
    return cmp(x,y)
