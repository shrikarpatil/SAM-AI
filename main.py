import pandas as pd
import numpy as np
import json
from ai_steps import generate_response

RHEL_ENTITLEMENTS = 20
VDC_ENTITLEMENTS = 21
entitlement_summary = [{
    'Product Name': 'Red Hat Enterprise Linux',
    'Entitlements': RHEL_ENTITLEMENTS,
}, {
    'Product Name': 'Red Hat Virtual Datacenter',
    'Entitlements': VDC_ENTITLEMENTS,
}]
entitlements = pd.DataFrame(entitlement_summary)

vInfo = pd.read_excel('input.xlsx', sheet_name='vInfo')
vHost = pd.read_excel('input.xlsx', sheet_name='vHost')
red_hat_vms = vInfo[vInfo["GuestOS"].str.contains("Red Hat", na=False, case=False)]

clusters = vHost['Cluster'].unique()

vdc_rows = []
rhel_rows = []
for cluster in clusters:
    number_of_hosts = len(vHost[vHost['Cluster'] == cluster])
    number_of_red_hat_vms = len(red_hat_vms[red_hat_vms['Cluster'] == cluster])
  
    if (number_of_red_hat_vms/number_of_hosts) >= 7:
        hosts = vHost[vHost['Cluster'] == cluster]['Host'].unique()
        
        for host in hosts :            
            vdc_rows.append({
                'Cluster': cluster,
                'Host': host,
                'Red Hat VMs': red_hat_vms[red_hat_vms['Host'] == host].shape[0]      
            })
    else:
        hosts = vHost[vHost['Cluster'] == cluster]['Host'].unique()
        for host in hosts :   
         rhel_rows.append({
            'Cluster': cluster,
            'Host': host,
            'Red Hat VMs': red_hat_vms[red_hat_vms['Host'] == host].shape[0]
        })

vdc = pd.DataFrame(vdc_rows)
vdc['Licenses Required'] = 1
rhel = pd.DataFrame(rhel_rows)

vdc_summary = {
    'Product Name': 'Red Hat Virtual Datacenter',
    'Entitlements': VDC_ENTITLEMENTS,
    'Deployments': vdc['Licenses Required'].sum(),
    'Effective License Position': VDC_ENTITLEMENTS - vdc['Licenses Required'].sum()
}
rhel_summary = {
    'Product Name': 'Red Hat Enterprise Linux',
    'Entitlements': RHEL_ENTITLEMENTS,
    'Deployments': np.ceil(rhel['Red Hat VMs'].sum()/2),
    'Effective License Position': RHEL_ENTITLEMENTS - np.ceil(rhel['Red Hat VMs'].sum()/2)
}

summary = [vdc_summary, rhel_summary]
elp = pd.DataFrame(summary)


print(vdc)
print(rhel)
print(elp)

ai_response = generate_response(entitlements, elp, rhel, vdc)
ai_json = json.loads(ai_response)
print("\nAI Response:\n")
print(ai_response)
comments = pd.DataFrame(ai_json)

with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    entitlements.to_excel(writer, sheet_name='Entitlements', index=False)
    elp.to_excel(writer, sheet_name='ELP', index=False)
    vdc.to_excel(writer, sheet_name='VDC', index=False)
    rhel.to_excel(writer, sheet_name='RHEL', index=False)
    comments.to_excel(writer,sheet_name='AI Comments', index=False)