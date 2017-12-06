# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:20:02 2017

@author: sjeyaven
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:13:14 2017

@author: sjeyaven
"""
from collections import defaultdict
import re
import pymysql
parent_child=defaultdict(list)
child=defaultdict(list)
database=defaultdict(list)
parent=defaultdict(list)
data=[]



with open("database-dumps-database-dump.sql",'r',encoding='Windows-1251') as x:
    print("DB and tables")
#wn database
    for line in x:
        db=re.match(r'(CREATE DATABASE)(.*)([`]{1})([a-z_]+)([`]{1})(.*)',line)    
        if db:
            Db=db.group(4)
            data=(db.group(4))+"."
            #print("%s(DB)"%(Db))
        #print(line)
        tables=re.match(r'^(CREATE TABLE)(.*)([`]{1})([a-zA-z0-9_]+)([`]{1})(.*)',line)
        constraint=re.match(r'(.*)(CONSTRAINT)(.*)(FOREIGN KEY)(.*)(`)(.*)(`)(.*)(REFERENCES )([`]{1})([a-zA-z0-9_]+)([`]{1})(.*)(`)(.*)(`)(.*)',line)
        #if constraint:
            #print(constraint.group(16))
        
        if tables:
            tab=tables.group(4)
            db_tab=data+tables.group(4)
            #print(tab)
            database[Db].append(db_tab)
            l={}
            k={}
            if db_tab not in parent_child.keys():
                parent_child[db_tab].append(l)
                parent_child[db_tab].append(k)
        if constraint and (db_tab!=data+constraint.group(12)):
             l[data+constraint.group(12)]=constraint.group(7)
             parent_child[db_tab][0].update(l)
             fk=data+constraint.group(12)
             l={}
             k={}
             if fk not in parent_child:
                 parent_child[fk].append(l)
                 parent_child[fk].append(k)
             if fk!=db_tab:
                 k[db_tab]=constraint.group(16)
                 parent_child[fk][1].update(k)
              
#print(parent_child)
parent_child_copy=parent_child.copy()
      
info=open("ab.txt","w")
info.write(str(parent_child))
info.close()


db=dict.copy(parent_child)

#sys.setrecursionlimit(3500)
list_track=[]
def recurs(a):
    #print(a)
    if a in db:
        for ele in db[a][1]:
            if ele and (ele not in db[a][0] and db[a][1]) and ele not in db[ele][0]:
                # print(ele)
                recurs(ele)
                
                if ele not in list_track:
                    
                    list_track.append(ele)
        if a not in list_track :
            list_track.append(a)        
    else:
        pass
    return list_track
def recurs_specific(a,list_):
    #print(a)
    if a in db:
        for ele in db[a][1]:
            if ele and (ele not in db[a][0] and db[a][1]) and ele not in db[ele][0]:
                # print(ele)
                recurs(ele)
                
                if ele not in list_:
                    
                    list_.append(ele)
        if a not in list_ :
            list_.append(a)        
    else:
        pass
    return list_
    


#db={'a':[{},{}],'b':[{},{'c':'None','d':'None'}],'c':[{'e':'None'},{'e':'None','f':'None'}],'e':[{},{'c':'None'}],'f':[{},{'g':'None','h':'None'}],'d':[{},{}],'g':[{},{'i':'None','j':'None'}],'h':[{},{}],'k':[{},{'l':'None','m':'None'}],'n':[{},{'o':'None','p':'None'}],'p':[{},{'q':'None','r':'None'}]}
#db={'t1':[[],['t2','t3']],'t2':[['t1','t2'],['t3','t4']],'t3':[['t2'],['t4']],'t4':[['t3'],['t2']]}
def tab_recurs(ip):
    output=[]
    list_=[]
#ip=input()
    if db[ip][1]:
        ls=db[ip][1]
        if ls:
            
            #print(list_ls)
            #print(ls)
            for a in ls.keys():
                list_=recurs_specific(a,list_)
            #list_track.append(a)
    output=list_
    output.append(ip)
    return(output)
tab_recurs("netapp_model.aggregate")


for k in db.keys():
	#print(k)

	if k not in list_track:
		#print(k)
		recurs(k)
  #print("h")
       #pass 
	else:
		pass
	
           
#print(list_track)
fp1=open('trail.html','w')
fp2=open('new.html','w')
fp3=open('final.html','w')

fp1.write("<html><head><link rel='stylesheet' href='styles.css'/><script src='jscript.js'></script></head><body><table id='database'border='1'><tr><th>Database Names</th></tr>")
for k,v in database.items():
   
    #fp1.write("---------\n")
    fp1.write("<tr><td><a href='#' id='"+k+"' value='"+k+"' class='target' data-info='"+k+"'onclick='myFunction(this.id)'>"+k+"</a></td></tr>")
    
    #fp1.write("Tables:\n")
    #fp1.write("---------\n")
    #for val in v:
     #   fp1.write(val+"\n")
fp1.write("</table><p id='info'></p></body></html>")
fp1.close()
conn =pymysql.connect(host='10.71.233.19',
                                       user='root',
                                       password='P@ssw0rd',
                                       db='netapp_model',
                                       cursorclass=pymysql.cursors.DictCursor)
fp2.write("<html><head><link rel='stylesheet' href='styles.css'></link><script src='jscript.js'></script></head><body onload='myfunc(this)'>")
try:
    with conn.cursor() as cursor:
        for k,v in database.items():
            if k=='netapp_model':
                fp2.write("<table class='tab' id='"+k+"' border='1'><tr><th>Table Names</th><th>Live objects</th><th>Dead objects</th></tr>")
            else:
                fp2.write("<table class='tab' id='"+k+"' border='1'><tr><th>Table Names</th><th>Count</th></tr>")
            for val in v:
                a=str(val.split('.')[1])
               # print(a)
                result=""
                if (k.split('.')[0]=='netapp_model'):
                    try:
                        cursor.execute("select count(*) from `%s` where `objState` like('LIVE')"%(a))
                        result=cursor.fetchone()
                        print(result['count(*)'])
                        cursor.execute("select count(*)from `%s` where `objState`='DEAD'"%(a))
                        dead=cursor.fetchone()
                        print(dead['count(*)'])
                        fp2.write("<tr><td><a href='#' id='"+val+"' value='"+val+"' data-info='"+val+"' onclick='myFunction_table(this.id)'>"+a+"</a></td><td>"+str(result['count(*)'])+"</td><td>"+str(dead['count(*)'])+"</td></tr>")
                    except pymysql.InternalError as error:
                        #print(error .args)
                        pass
                else:
                    fp2.write("<tr><td><a href='#' id='"+val+"' value='"+val+"' data-info='"+val+"' onclick='myFunction_table(this.id)'>"+a+"</a></td></tr>")
        
            fp2.write("</table></body></html>")
except pymysql.InternalError as error:
    #print(error .args)
    pass
conn.close()
fp2.close()
#print(database)
fp3.write("<html><head><link rel='stylesheet' href='styles.css'></link><script src='jscript.js'></script></head><body onload='myfunc1(this)'>")
#print(parent_child)
for k,v in parent_child.items():
    #fp1.write("\nTable:"+k+"\n")
    del_order=tab_recurs(k)
    fp3.write("<table class='tab' id='"+str(k)+"' value='"+k+"'  border='1'><th>Table name'"+str(k)+"'</th><tr><th>Parent Table</th><th>Child Table</th><th>Deletion Order</th></tr>")
    #for val in v:
    #print(k)
    if val:
        fp3.write("<tr><td>")
        for parent_value in parent_child[k][0]:
            #print(parent_value)
            fp3.write("<a href='#' onclick="+"myFunction_parent('"+parent_value+"')>"+str(parent_value.split('.')[1])+"</a><br>")
        fp3.write("</td><td>")
        if parent_child[k][1]:
                #fp2.write("Child\n")
            for a in parent_child[k][1]:
                    #print (a)
                fp3.write("<a href='#' onclick="+"myFunction_parent('"+a+"')>"+str(a.split('.')[1])+"</a><br>")
            
            fp3.write("</td>")
        #fp1.write("<td>"+str(del_order)+"</td>")
        
        fp3.write("<td >"+str(del_order)+"</td>"+"</tr>")
    

fp3.write("</table>")    
fp3.write("</body></html>")
fp3.close()


    
import pymysql
#from mysql.connector import Error

fp=open("inconsitency.txt",'w')
def connect(a_db,tab_only,tab,**dd):
    """ Connect to MySQL database """
    
    conn =pymysql.connect(host='10.71.233.19',
                                       user='root',
                                       password='P@ssw0rd',
                                       db=a_db,
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            #count=0
            # if conn.is_connected():
            #   print('Connected to MySQL database')
            if tab in dd.keys():
                     #print(dd.keys())
                        for a in dd[tab][0]:
                            if a:
                                fk=dd[tab][0][a]
                                b=dd[a][1]
                                #print(b)
                                #print(a)
                                if tab in b:
                                    #print("Parent:"+a.split(".")[1]+"\n"+"Child:"+tab+"\n")
                                    pk=dd[a][1][tab]
                                    #print(fk+"\n"+pk)
                                    if fk and pk:
                                        #count=count+1
                                        cursor.execute("SELECT * FROM `%s` WHERE `%s` IN (SELECT `%s` FROM `%s` WHERE `objState`='DEAD') AND `objState`='LIVE'"%(tab_only,fk,pk,a.split(".")[1]))
                                        #print(cursor.rowcount)
                                        
                                        #row =cursor.fetchone()
                                        #length=len(cursor.fetchall())
                                        rows=cursor.fetchall()
                                        #length=len(cursor.fetchall())
                                        if rows:
                                            #length=len(cursor.fetchall())
                                            #print(length)
                                            fp.write(tab_only+"(child)"+"->"+a.split(".")[1]+"(Parent)"+"has "+str(len(rows))+" Inconsistencies"+" Foreign key constraint-"+str(fk)+"\n")
                                            #while row is not None:
                                            #rows=cursor.fetchall()
                                            for k in rows: 
                                            #fp.write(str(row)+"\n")
                                               # row = cursor.fetchone()
                                                fp.write(str(k)+"\n") 
            else:
                #print("No parent table")
                pass
                    
                    
            
                    
    except pymysql.InternalError as error:
        #print(error .args)
        pass
    conn.close()
    #print(count)
                #finally:
                 #   
    

            
        

parent_child={'acquisition.acquisition_storage_identify': [{}, {}], 'acquisition.acquisition_volume_identify': [{}, {}], 'acquisition.au': [{}, {'acquisition.au_attrs': 'id', 'acquisition.au_audit': 'id', 'acquisition.ds': 'id'}], 'acquisition.au_attrs': [{'acquisition.au': 'au_id'}, {}], 'acquisition.au_audit': [{'acquisition.au': 'au_id'}, {}], 'acquisition.ds': [{'acquisition.au': 'au_id'}, {'acquisition.ds_attrs': 'id', 'acquisition.originator': 'id'}], 'acquisition.ds_attrs': [{'acquisition.ds': 'ds_id'}, {}], 'acquisition.ds_audit': [{}, {'acquisition.ds_audit_details': 'id'}], 'acquisition.ds_audit_details': [{'acquisition.ds_audit': 'audit_id'}, {}], 'acquisition.ds_type': [{}, {'acquisition.ds_type_attrs': 'id', 'acquisition.ds_type_vendormodel': 'id'}], 'acquisition.ds_type_attrs': [{'acquisition.ds_type': 'ds_type_id'}, {}], 'acquisition.ds_type_vendormodel': [{'acquisition.ds_type': 'ds_type_id'}, {}], 'acquisition.originator': [{'acquisition.ds': 'ds_id'}, {}], 'management.id': [{}, {}], 'management.info': [{}, {}], 'management.scale': [{}, {}], 'management.version': [{}, {}], 'mysql.columns_priv': [{}, {}], 'mysql.db': [{}, {}], 'mysql.event': [{}, {}], 'mysql.func': [{}, {}], 'mysql.help_category': [{}, {}], 'mysql.help_keyword': [{}, {}], 'mysql.help_relation': [{}, {}], 'mysql.help_topic': [{}, {}], 'mysql.host': [{}, {}], 'mysql.innodb_index_stats': [{}, {}], 'mysql.innodb_table_stats': [{}, {}], 'mysql.ndb_binlog_index': [{}, {}], 'mysql.plugin': [{}, {}], 'mysql.proc': [{}, {}], 'mysql.procs_priv': [{}, {}], 'mysql.proxies_priv': [{}, {}], 'mysql.servers': [{}, {}], 'mysql.slave_master_info': [{}, {}], 'mysql.slave_relay_log_info': [{}, {}], 'mysql.slave_worker_info': [{}, {}], 'mysql.tables_priv': [{}, {}], 'mysql.time_zone': [{}, {}], 'mysql.time_zone_leap_second': [{}, {}], 'mysql.time_zone_name': [{}, {}], 'mysql.time_zone_transition': [{}, {}], 'mysql.time_zone_transition_type': [{}, {}], 'mysql.user': [{}, {}], 'mysql.general_log': [{}, {}], 'mysql.slow_log': [{}, {}], 'netapp_model.aggregate': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {'netapp_model.disk_aggregate_relationship': 'objid', 'netapp_model.plex': 'objid', 'netapp_model.qos_service_center': 'objid', 'netapp_model.raid_group': 'objid', 'netapp_model.resource_aggregate': 'objid', 'netapp_model.storage_pool_aggregate_relationship': 'objid', 'netapp_model.volume': 'objid', 'netapp_model.volume_move_job': 'objid', 'netapp_model.vserver_to_aggregate': 'objid'}], 'netapp_model.cluster': [{'netapp_model.node': 'nodeId'}, {'netapp_model.aggregate': 'objid', 'netapp_model.application_record': 'objid', 'netapp_model.cifs_share_acl': 'objid', 'netapp_model.cluster_peer': 'objid', 'netapp_model.disk': 'objid', 'netapp_model.disk_aggregate_relationship': 'objid', 'netapp_model.disk_path': 'objid', 'netapp_model.export_policy': 'objid', 'netapp_model.export_rule': 'objid', 'netapp_model.fcp_lif': 'objid', 'netapp_model.fcp_port': 'objid', 'netapp_model.flash_device': 'objid', 'netapp_model.igroup': 'objid', 'netapp_model.igroup_initiator': 'objid', 'netapp_model.iscsi_portal_group': 'objid', 'netapp_model.iscsi_portal_group_lif': 'objid', 'netapp_model.iscsi_security_entry': 'objid', 'netapp_model.iscsi_session': 'objid', 'netapp_model.iscsi_session_connection': 'objid', 'netapp_model.job_schedule': 'objid', 'netapp_model.license': 'objid', 'netapp_model.license_v2_entitlement_risk': 'objid', 'netapp_model.lif': 'objid', 'netapp_model.lun': 'objid', 'netapp_model.lun_import': 'objid', 'netapp_model.lun_map': 'objid', 'netapp_model.lun_map_reporting_node': 'objid', 'netapp_model.metrocluster_operation': 'objid', 'netapp_model.network_failover_group': 'objid', 'netapp_model.network_failover_group_network_port_relationship': 'objid', 'netapp_model.network_ip_space': 'objid', 'netapp_model.network_lif': 'objid', 'netapp_model.network_port': 'objid', 'netapp_model.network_port_broadcast_domain': 'objid', 'netapp_model.network_route': 'objid', 'netapp_model.network_route_lif': 'objid', 'netapp_model.network_subnet': 'objid', 'netapp_model.nis_domain': 'objid', 'netapp_model.node': 'objid', 'netapp_model.node_license_usage': 'objid', 'netapp_model.plex': 'objid', 'netapp_model.portset': 'objid', 'netapp_model.portset_port': 'objid', 'netapp_model.portset_to_igroup': 'objid', 'netapp_model.processor': 'objid', 'netapp_model.qos_policy_group': 'objid', 'netapp_model.qos_service_center': 'objid', 'netapp_model.qos_volume_workload': 'objid', 'netapp_model.qos_workload_detail': 'objid', 'netapp_model.qos_workload_node_relationship': 'objid', 'netapp_model.qtree': 'objid', 'netapp_model.qtree_quota': 'objid', 'netapp_model.quota_user': 'objid', 'netapp_model.raid_group': 'objid', 'netapp_model.resource_aggregate': 'objid', 'netapp_model.routing_group': 'objid', 'netapp_model.routing_group_destination': 'objid', 'netapp_model.service_processor': 'objid', 'netapp_model.sis_policy': 'objid', 'netapp_model.snap_mirror': 'objid', 'netapp_model.snap_mirror_history': 'objid', 'netapp_model.snap_mirror_policy': 'objid', 'netapp_model.snap_mirror_policy_rule': 'objid', 'netapp_model.snaplock': 'objid', 'netapp_model.snapshot': 'objid', 'netapp_model.snapshot_policy': 'objid', 'netapp_model.snapshot_policy_schedule': 'objid', 'netapp_model.storage_adapter': 'objid', 'netapp_model.storage_pool': 'objid', 'netapp_model.storage_pool_aggregate_relationship': 'objid', 'netapp_model.storage_pool_available': 'objid', 'netapp_model.storage_service': 'objid', 'netapp_model.storage_shelf': 'objid', 'netapp_model.storage_shelf_cable': 'objid', 'netapp_model.storage_switch': 'objid', 'netapp_model.system_health_alert': 'objid', 'netapp_model.user_quota': 'objid', 'netapp_model.volume': 'objid', 'netapp_model.volume_move_job': 'objid', 'netapp_model.vserver': 'objid', 'netapp_model.vserver_name_mapping': 'objid', 'netapp_model.vserver_peer': 'objid', 'netapp_model.vserver_to_aggregate': 'objid'}], 'netapp_model.node': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.aggregate': 'objid', 'netapp_model.disk': 'objid', 'netapp_model.disk_path': 'objid', 'netapp_model.fcp_port': 'objid', 'netapp_model.flash_device': 'objid', 'netapp_model.ha_pair': 'objid', 'netapp_model.license': 'objid', 'netapp_model.lif': 'objid', 'netapp_model.lun_import': 'objid', 'netapp_model.lun_map': 'objid', 'netapp_model.lun_map_reporting_node': 'objid', 'netapp_model.metrocluster_operation': 'objid', 'netapp_model.network_port': 'objid', 'netapp_model.node_license_usage': 'objid', 'netapp_model.plex': 'objid', 'netapp_model.processor': 'objid', 'netapp_model.qos_service_center': 'objid', 'netapp_model.qos_workload_node_relationship': 'objid', 'netapp_model.raid_group': 'objid', 'netapp_model.service_processor': 'objid', 'netapp_model.snap_mirror': 'objid', 'netapp_model.storage_adapter': 'objid', 'netapp_model.storage_pool_available': 'objid', 'netapp_model.storage_shelf': 'objid', 'netapp_model.storage_shelf_cable': 'objid', 'netapp_model.system_health_alert': 'objid'}], 'netapp_model.application_record': [{'netapp_model.cluster': 'clusterId'}, {}], 'netapp_model.bak_qos_workload_constituent': [{}, {}], 'netapp_model.bak_qos_workload_detail': [{}, {}], 'netapp_model.change_delete_detail': [{}, {}], 'netapp_model.change_record': [{}, {}], 'netapp_model.changed_attribute': [{}, {}], 'netapp_model.cifs_share': [{}, {'netapp_model.cifs_share_acl': 'objid'}], 'netapp_model.cifs_share_acl': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.cifs_share': 'cifsShareId'}, {}], 'netapp_model.vserver': [{'netapp_model.cifs_share': 'cifsShareId', 'netapp_model.cluster': 'clusterId', 'netapp_model.snapshot_policy': 'snapshotPolicyId', 'netapp_model.qos_policy_group': 'qosPolicyGroupId', 'netapp_model.network_ip_space': 'networkIpSpaceId'}, {'netapp_model.cifs_share_acl': 'objid', 'netapp_model.export_policy': 'objid', 'netapp_model.export_rule': 'objid', 'netapp_model.fcp_lif': 'objid', 'netapp_model.igroup': 'objid', 'netapp_model.igroup_initiator': 'objid', 'netapp_model.iscsi_portal_group': 'objid', 'netapp_model.iscsi_portal_group_lif': 'objid', 'netapp_model.iscsi_security_entry': 'objid', 'netapp_model.lif': 'objid', 'netapp_model.lun': 'objid', 'netapp_model.lun_import': 'objid', 'netapp_model.lun_map': 'objid', 'netapp_model.network_failover_group': 'objid', 'netapp_model.network_lif': 'objid', 'netapp_model.network_route': 'objid', 'netapp_model.nis_domain': 'objid', 'netapp_model.portset': 'objid', 'netapp_model.qos_policy_group_vserver_relationship': 'objid', 'netapp_model.qos_volume_workload': 'objid', 'netapp_model.qtree': 'objid', 'netapp_model.qtree_quota': 'objid', 'netapp_model.quota_user': 'objid', 'netapp_model.routing_group': 'objid', 'netapp_model.routing_group_destination': 'objid', 'netapp_model.sis_policy': 'objid', 'netapp_model.snap_mirror': 'objid', 'netapp_model.snap_mirror_policy': 'objid', 'netapp_model.snapshot': 'objid', 'netapp_model.snapshot_policy_vserver_relationship': 'objid', 'netapp_model.storage_service': 'objid', 'netapp_model.user_quota': 'objid', 'netapp_model.volume': 'objid', 'netapp_model.vserver_name_mapping': 'objid', 'netapp_model.vserver_peer': 'objid', 'netapp_model.vserver_to_aggregate': 'objid'}], 'netapp_model.cluster_peer': [{'netapp_model.cluster': 'remoteClusterId', 'netapp_model.network_ip_space': 'networkIpSpaceId'}, {}], 'netapp_model.network_ip_space': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.cluster_peer': 'objid', 'netapp_model.network_port': 'objid', 'netapp_model.network_port_broadcast_domain': 'objid', 'netapp_model.network_subnet': 'objid', 'netapp_model.vserver': 'objid'}], 'netapp_model.disk': [{'netapp_model.cluster': 'clusterId', 'netapp_model.raid_group': 'raidGroupId', 'netapp_model.node': 'homeNodeId', 'netapp_model.storage_pool': 'storagePoolId'}, {'netapp_model.disk_aggregate_relationship': 'objid', 'netapp_model.disk_path': 'objid', 'netapp_model.lun_import': 'objid'}], 'netapp_model.raid_group': [{'netapp_model.node': 'nodeId', 'netapp_model.plex': 'plexId', 'netapp_model.aggregate': 'aggregateId', 'netapp_model.cluster': 'clusterId'}, {'netapp_model.disk': 'objid'}], 'netapp_model.storage_pool': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.disk': 'objid', 'netapp_model.storage_pool_aggregate_relationship': 'objid', 'netapp_model.storage_pool_available': 'objid'}], 'netapp_model.disk_aggregate_relationship': [{'netapp_model.cluster': 'clusterId', 'netapp_model.disk': 'diskId', 'netapp_model.aggregate': 'aggregateId'}, {}], 'netapp_model.disk_path': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId', 'netapp_model.disk': 'diskId', 'netapp_model.storage_adapter': 'initiatorPortId'}, {}], 'netapp_model.storage_adapter': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {'netapp_model.disk_path': 'objid'}], 'netapp_model.export_policy': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.export_rule': 'objid', 'netapp_model.qtree': 'objid', 'netapp_model.volume': 'objid'}], 'netapp_model.export_rule': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.export_policy': 'exportPolicyId'}, {}], 'netapp_model.fcp_lif': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.fcp_port': 'homePortId'}, {'netapp_model.portset_port': 'objid'}], 'netapp_model.fcp_port': [{'netapp_model.fcp_port': 'homePortId', 'netapp_model.node': 'nodeId', 'netapp_model.cluster': 'clusterId'}, {'netapp_model.fcp_lif': 'objid'}], 'netapp_model.flash_device': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.ha_pair': [{'netapp_model.node': 'node2Id'}, {}], 'netapp_model.igroup': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.igroup_initiator': 'objid', 'netapp_model.lun_map': 'objid', 'netapp_model.portset_to_igroup': 'objid'}], 'netapp_model.igroup_initiator': [{'netapp_model.cluster': 'clusterId', 'netapp_model.igroup': 'igroupId', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.iscsi_portal_group': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.iscsi_portal_group_lif': 'objid', 'netapp_model.iscsi_session': 'objid', 'netapp_model.portset_port': 'objid'}], 'netapp_model.iscsi_portal_group_lif': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.iscsi_portal_group': 'targetPortalGroupId', 'netapp_model.network_lif': 'lifId'}, {}], 'netapp_model.network_lif': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.network_port': 'homePortId', 'netapp_model.routing_group': 'routingGroupId'}, {'netapp_model.iscsi_portal_group_lif': 'objid', 'netapp_model.iscsi_session_connection': 'objid'}], 'netapp_model.iscsi_security_entry': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.iscsi_session': [{'netapp_model.cluster': 'clusterId', 'netapp_model.iscsi_portal_group': 'targetPortalGroupId'}, {'netapp_model.iscsi_session_connection': 'objid'}], 'netapp_model.iscsi_session_connection': [{'netapp_model.cluster': 'clusterId', 'netapp_model.iscsi_session': 'iscsiSessionId', 'netapp_model.network_lif': 'lifId'}, {}], 'netapp_model.job_schedule': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.sis_policy': 'objid', 'netapp_model.snap_mirror': 'objid', 'netapp_model.snapshot_policy_schedule': 'objid'}], 'netapp_model.license': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'ownerNodeId'}, {}], 'netapp_model.license_v2_entitlement_risk': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.node_license_usage': 'objid'}], 'netapp_model.lif': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'homeNodeId', 'netapp_model.vserver': 'vserverId', 'netapp_model.network_failover_group': 'failoverGroupId'}, {'netapp_model.network_route_lif': 'objid'}], 'netapp_model.network_failover_group': [{'netapp_model.cluster': 'clusterId', 'netapp_model.network_port_broadcast_domain': 'networkPortBroadcastDomainId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.lif': 'objid', 'netapp_model.network_failover_group_network_port_relationship': 'objid'}], 'netapp_model.lun': [{'netapp_model.qtree': 'qtreeId', 'netapp_model.volume': 'volumeId', 'netapp_model.vserver': 'vserverId', 'netapp_model.cluster': 'clusterId', 'netapp_model.qos_policy_group': 'qosPolicyGroupId'}, {'netapp_model.lun_map': 'objid'}], 'netapp_model.qtree': [{'netapp_model.volume': 'volumeId', 'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.export_policy': 'exportPolicyId'}, {'netapp_model.lun': 'objid', 'netapp_model.qtree_quota': 'objid', 'netapp_model.user_quota': 'objid'}], 'netapp_model.volume': [{'netapp_model.vserver': 'vserverId', 'netapp_model.cluster': 'clusterId', 'netapp_model.aggregate': 'aggregateId', 'netapp_model.export_policy': 'exportPolicyId', 'netapp_model.snapshot_policy': 'snapshotPolicyId', 'netapp_model.sis_policy': 'sisPolicyId', 'netapp_model.storage_service': 'storageServiceId', 'netapp_model.qos_policy_group': 'qosPolicyGroupId'}, {'netapp_model.lun': 'objid', 'netapp_model.qos_volume_workload': 'objid', 'netapp_model.qtree': 'objid', 'netapp_model.qtree_quota': 'objid', 'netapp_model.snap_mirror': 'objid', 'netapp_model.snaplock': 'objid', 'netapp_model.snapshot': 'objid', 'netapp_model.user_quota': 'objid', 'netapp_model.volume_flexcache': 'objid', 'netapp_model.volume_flexgroup_constituent_relationship': 'objid', 'netapp_model.volume_move_job': 'objid', 'netapp_model.volume_self_relationship': 'objid'}], 'netapp_model.qos_policy_group': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.lun': 'objid', 'netapp_model.qos_policy_group_vserver_relationship': 'objid', 'netapp_model.volume': 'objid', 'netapp_model.vserver': 'objid'}], 'netapp_model.lun_import': [{'netapp_model.vserver': 'vserverId', 'netapp_model.cluster': 'clusterId', 'netapp_model.disk': 'foreignDiskId', 'netapp_model.node': 'importHomeNodeId'}, {}], 'netapp_model.lun_map': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.igroup': 'igroupId', 'netapp_model.lun': 'lunId', 'netapp_model.node': 'owningNodeId'}, {'netapp_model.lun_map_reporting_node': 'objid'}], 'netapp_model.lun_map_reporting_node': [{'netapp_model.cluster': 'clusterId', 'netapp_model.lun_map': 'lunMapId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.metrocluster_operation': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeID'}, {}], 'netapp_model.network_port_broadcast_domain': [{'netapp_model.vserver': 'vserverId', 'netapp_model.cluster': 'clusterId', 'netapp_model.network_ip_space': 'networkIpSpaceId'}, {'netapp_model.network_failover_group': 'objid', 'netapp_model.network_port': 'objid', 'netapp_model.network_subnet': 'objid'}], 'netapp_model.network_failover_group_network_port_relationship': [{'netapp_model.cluster': 'clusterId', 'netapp_model.network_failover_group': 'networkFailoverGroupId', 'netapp_model.network_port': 'networkPortId'}, {}], 'netapp_model.network_port': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId', 'netapp_model.network_ip_space': 'networkIpSpaceId', 'netapp_model.network_port_broadcast_domain': 'networkPortBroadcastDomainId'}, {'netapp_model.network_failover_group_network_port_relationship': 'objid', 'netapp_model.network_lif': 'objid', 'netapp_model.network_port_relationship': 'objid'}], 'netapp_model.routing_group': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.network_lif': 'objid', 'netapp_model.routing_group_destination': 'objid'}], 'netapp_model.network_port_relationship': [{'netapp_model.network_port': 'objid'}, {}], 'netapp_model.network_route': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.network_route_lif': 'objid'}], 'netapp_model.network_route_lif': [{'netapp_model.cluster': 'clusterId', 'netapp_model.network_route': 'networkRouteId', 'netapp_model.lif': 'lifId'}, {}], 'netapp_model.network_subnet': [{'netapp_model.cluster': 'clusterId', 'netapp_model.network_ip_space': 'ipspaceId', 'netapp_model.network_port_broadcast_domain': 'broadcastDomainId'}, {}], 'netapp_model.nis_domain': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.node_license_usage': [{'netapp_model.cluster': 'clusterId', 'netapp_model.license_v2_entitlement_risk': 'licenseV2EntitlementRiskId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.param': [{}, {}], 'netapp_model.plex': [{'netapp_model.aggregate': 'aggregateId', 'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {'netapp_model.raid_group': 'objid'}], 'netapp_model.portset': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.portset_port': 'objid', 'netapp_model.portset_to_igroup': 'objid'}], 'netapp_model.portset_port': [{'netapp_model.cluster': 'clusterId', 'netapp_model.portset': 'portsetId', 'netapp_model.fcp_lif': 'fcpLifId', 'netapp_model.iscsi_portal_group': 'iSCSIPortalGroupId'}, {}], 'netapp_model.portset_to_igroup': [{'netapp_model.cluster': 'clusterId', 'netapp_model.portset': 'portsetId', 'netapp_model.igroup': 'igroupId'}, {}], 'netapp_model.processor': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.qos_policy_group_vserver_relationship': [{'netapp_model.qos_policy_group': 'objid', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.qos_service_center': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId', 'netapp_model.aggregate': 'aggregateId'}, {'netapp_model.qos_service_center_relationship': 'objid', 'netapp_model.qos_workload_detail': 'objid'}], 'netapp_model.qos_service_center_relationship': [{'netapp_model.qos_service_center': 'parentQosServiceCenterId'}, {}], 'netapp_model.qos_volume_workload': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.volume': 'volumeId'}, {'netapp_model.qos_workload_detail': 'objid', 'netapp_model.qos_workload_node_relationship': 'objid'}], 'netapp_model.qos_workload_detail': [{'netapp_model.cluster': 'clusterId', 'netapp_model.qos_volume_workload': 'workloadId', 'netapp_model.qos_service_center': 'serviceCenterId'}, {}], 'netapp_model.qos_workload_node_relationship': [{'netapp_model.cluster': 'clusterId', 'netapp_model.qos_volume_workload': 'workloadId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.qtree_quota': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.volume': 'volumeId', 'netapp_model.qtree': 'qtreeId'}, {}], 'netapp_model.quota_user': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.user_quota': 'userQuotaId'}, {}], 'netapp_model.user_quota': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.volume': 'volumeId', 'netapp_model.qtree': 'qtreeId'}, {'netapp_model.quota_user': 'objid'}], 'netapp_model.resource_aggregate': [{'netapp_model.cluster': 'clusterId', 'netapp_model.aggregate': 'aggregateId'}, {}], 'netapp_model.routing_group_destination': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.routing_group': 'routingGroupId'}, {}], 'netapp_model.service_processor': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.sis_policy': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.job_schedule': 'jobScheduleId'}, {'netapp_model.volume': 'objid'}], 'netapp_model.snap_mirror': [{'netapp_model.job_schedule': 'jobScheduleId', 'netapp_model.cluster': 'sourceClusterId', 'netapp_model.vserver': 'sourceVserverId', 'netapp_model.volume': 'sourceVolumeId', 'netapp_model.node': 'nodeId', 'netapp_model.snapshot': 'newestSnapshotId', 'netapp_model.snap_mirror_policy': 'snapMirrorPolicyId'}, {'netapp_model.snap_mirror_history': 'objid', 'netapp_model.snap_mirror_self_relationship': 'objid'}], 'netapp_model.snapshot': [{'netapp_model.snapshot': 'newestSnapshotId', 'netapp_model.volume': 'volumeId', 'netapp_model.vserver': 'vserverId', 'netapp_model.cluster': 'clusterId'}, {'netapp_model.snap_mirror': 'objid'}], 'netapp_model.snap_mirror_policy': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.snap_mirror': 'objid', 'netapp_model.snap_mirror_policy_rule': 'objid'}], 'netapp_model.snap_mirror_history': [{'netapp_model.cluster': 'clusterId', 'netapp_model.snap_mirror': 'snapMirrorId'}, {}], 'netapp_model.snap_mirror_policy_rule': [{'netapp_model.cluster': 'clusterId', 'netapp_model.snap_mirror_policy': 'snapMirrorPolicyId'}, {}], 'netapp_model.snap_mirror_self_relationship': [{'netapp_model.snap_mirror': 'vserverSnapMirrorId'}, {}], 'netapp_model.snaplock': [{'netapp_model.cluster': 'clusterId', 'netapp_model.volume': 'volumeId'}, {}], 'netapp_model.snapshot_policy': [{'netapp_model.cluster': 'clusterId'}, {'netapp_model.snapshot_policy_schedule': 'objid', 'netapp_model.snapshot_policy_vserver_relationship': 'objid', 'netapp_model.volume': 'objid', 'netapp_model.vserver': 'objid'}], 'netapp_model.snapshot_policy_schedule': [{'netapp_model.snapshot_policy': 'snapshotPolicyId', 'netapp_model.cluster': 'clusterId', 'netapp_model.job_schedule': 'jobScheduleId'}, {}], 'netapp_model.snapshot_policy_vserver_relationship': [{'netapp_model.snapshot_policy': 'objid', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.storage_pool_aggregate_relationship': [{'netapp_model.cluster': 'clusterId', 'netapp_model.storage_pool': 'storagePoolId', 'netapp_model.aggregate': 'aggregateId'}, {}], 'netapp_model.storage_pool_available': [{'netapp_model.cluster': 'clusterId', 'netapp_model.storage_pool': 'storagePoolId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.storage_service': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {'netapp_model.storage_service_volume_relationship': 'objid', 'netapp_model.volume': 'objid'}], 'netapp_model.storage_service_volume_relationship': [{'netapp_model.storage_service': 'objid'}, {}], 'netapp_model.storage_shelf': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {'netapp_model.storage_shelf_cable': 'objid'}], 'netapp_model.storage_shelf_cable': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId', 'netapp_model.storage_shelf': 'shelfId'}, {}], 'netapp_model.storage_switch': [{'netapp_model.cluster': 'clusterId'}, {}], 'netapp_model.system_health_alert': [{'netapp_model.cluster': 'clusterId', 'netapp_model.node': 'nodeId'}, {}], 'netapp_model.update_history': [{}, {}], 'netapp_model.upgrade_history': [{}, {}], 'netapp_model.version': [{}, {}], 'netapp_model.volume_flexcache': [{'netapp_model.volume': 'originVolumeId'}, {}], 'netapp_model.volume_flexgroup_constituent_relationship': [{'netapp_model.volume': 'flexgroupId'}, {}], 'netapp_model.volume_move_job': [{'netapp_model.cluster': 'clusterId', 'netapp_model.volume': 'volumeId', 'netapp_model.aggregate': 'destinationAggregateId'}, {}], 'netapp_model.volume_self_relationship': [{'netapp_model.volume': 'junctionParentId'}, {}], 'netapp_model.vserver_name_mapping': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId'}, {}], 'netapp_model.vserver_peer': [{'netapp_model.vserver': 'peerVServerId', 'netapp_model.cluster': 'peerClusterId'}, {}], 'netapp_model.vserver_to_aggregate': [{'netapp_model.cluster': 'clusterId', 'netapp_model.vserver': 'vserverId', 'netapp_model.aggregate': 'aggregateId'}, {}], 'netapp_performance.sample_current_disk': [{}, {}], 'netapp_performance.sample_current_fcplif': [{}, {}], 'netapp_performance.sample_current_fcpport': [{}, {}], 'netapp_performance.sample_current_iscsilif': [{}, {}], 'netapp_performance.sample_current_lun': [{}, {}], 'netapp_performance.sample_current_networklif': [{}, {}], 'netapp_performance.sample_current_networkport': [{}, {}], 'netapp_performance.sample_current_node': [{}, {}], 'netapp_performance.sample_current_processor': [{}, {}], 'netapp_performance.sample_current_qos_service_center': [{}, {}], 'netapp_performance.sample_current_qos_volume_workload': [{}, {}], 'netapp_performance.sample_current_qos_workload_detail': [{}, {}], 'netapp_performance.sample_current_qos_workload_queue_dblade': [{}, {}], 'netapp_performance.sample_current_qos_workload_queue_nblade': [{}, {}], 'netapp_performance.sample_current_status': [{}, {}], 'netapp_performance.sample_current_volume': [{}, {}], 'netapp_performance.sample_current_vserver': [{}, {}], 'netapp_performance.sample_qos_service_center_1': [{}, {}], 'netapp_performance.sample_qos_service_center_645': [{}, {}], 'netapp_performance.sample_qos_volume_workload_1': [{}, {}], 'netapp_performance.sample_qos_volume_workload_645': [{}, {}], 'netapp_performance.sample_qos_workload_detail_1': [{}, {}], 'netapp_performance.sample_qos_workload_detail_645': [{}, {}], 'netapp_performance.sample_qos_workload_queue_dblade_1': [{}, {}], 'netapp_performance.sample_qos_workload_queue_dblade_645': [{}, {}], 'netapp_performance.sample_qos_workload_queue_nblade_1': [{}, {}], 'netapp_performance.sample_qos_workload_queue_nblade_645': [{}, {}], 'netapp_performance.summary_daily_qos_volume_workload_1': [{}, {}], 'netapp_performance.summary_daily_qos_volume_workload_645': [{}, {}], 'netapp_performance.summary_qos_service_center_1': [{}, {}], 'netapp_performance.summary_qos_service_center_645': [{}, {}], 'netapp_performance.summary_qos_volume_workload_1': [{}, {}], 'netapp_performance.summary_qos_volume_workload_645': [{}, {}], 'netapp_performance.summary_qos_workload_detail_1': [{}, {}], 'netapp_performance.summary_qos_workload_detail_645': [{}, {}], 'netapp_performance.summary_qos_workload_queue_dblade_1': [{}, {}], 'netapp_performance.summary_qos_workload_queue_dblade_645': [{}, {}], 'netapp_performance.summary_qos_workload_queue_nblade_1': [{}, {}], 'netapp_performance.summary_qos_workload_queue_nblade_645': [{}, {}], 'netapp_performance.update_history': [{}, {}], 'ocum.aggregate': [{}, {'ocum.aggregategrowthrateinfo': 'id', 'ocum.aggregatehistorymonth': 'id', 'ocum.aggregatehistoryweek': 'id', 'ocum.aggregatehistoryyear': 'id', 'ocum.aggregateregressioninfo': 'id', 'ocum.diskaggregaterelationship': 'id', 'ocum.resourcepoolaggregates': 'id'}], 'ocum.aggregategrowthrateinfo': [{'ocum.aggregate': 'aggregate_id'}, {}], 'ocum.aggregatehistorymonth': [{'ocum.aggregate': 'aggregateId'}, {}], 'ocum.aggregatehistoryweek': [{'ocum.aggregate': 'aggregateId'}, {}], 'ocum.aggregatehistoryyear': [{'ocum.aggregate': 'aggregateId'}, {}], 'ocum.aggregateregressioninfo': [{'ocum.aggregate': 'aggregate_id'}, {}], 'ocum.alert': [{'ocum.script': 'scriptId'}, {'ocum.alert_emailaddressrecipients': 'id', 'ocum.alert_emailadminrecipients': 'id', 'ocum.alert_eventseverities': 'id', 'ocum.alerteventtypevalues': 'id', 'ocum.alertresourceobjects': 'id'}], 'ocum.script': [{}, {'ocum.alert': 'id'}], 'ocum.alert_emailaddressrecipients': [{'ocum.alert': 'alert_id'}, {}], 'ocum.alert_emailadminrecipients': [{'ocum.alert': 'alert_id', 'ocum.authorizationunit': 'authorizationUnit_id'}, {}], 'ocum.authorizationunit': [{'ocum.role': 'role_id'}, {'ocum.alert_emailadminrecipients': 'id'}], 'ocum.alert_eventseverities': [{'ocum.alert': 'alert_id'}, {}], 'ocum.alerteventtypevalues': [{'ocum.alert': 'alert_id', 'ocum.eventtypevalue': 'eventTypeValue_id'}, {}], 'ocum.eventtypevalue': [{'ocum.eventtype': 'type_id'}, {'ocum.alerteventtypevalues': 'id', 'ocum.customeventtypevalue': 'id', 'ocum.event': 'id'}], 'ocum.alertresourceobjects': [{'ocum.alert': 'alert_id'}, {}], 'ocum.annotation': [{'ocum.annotationtype': 'type_id'}, {'ocum.annotationmanualresourcemapping': 'id', 'ocum.annotationresourceobject': 'id', 'ocum.annotationrule': 'id'}], 'ocum.annotationtype': [{}, {'ocum.annotation': 'id', 'ocum.annotationrule': 'id'}], 'ocum.annotationmanualresourcemapping': [{'ocum.annotation': 'annotationValueId'}, {}], 'ocum.annotationofcluster': [{}, {}], 'ocum.annotationofvolume': [{}, {}], 'ocum.annotationofvserver': [{}, {}], 'ocum.annotationresourceobject': [{'ocum.annotation': 'annotation_id'}, {}], 'ocum.annotationrule': [{'ocum.annotationtype': 'annotationTypeId', 'ocum.annotation': 'annotationValueId'}, {'ocum.selectioncriterion': 'id'}], 'ocum.role': [{}, {'ocum.authorizationunit': 'id'}], 'ocum.backupfileinfo': [{}, {}], 'ocum.bridge': [{}, {'ocum.bridgestackconnection': 'id', 'ocum.nodebridgeconnection': 'id', 'ocum.switchbridgeconnection': 'id'}], 'ocum.bridgestackconnection': [{'ocum.bridge': 'bridge_id'}, {'ocum.bridgestacklink': 'id'}], 'ocum.bridgestacklink': [{'ocum.bridgestackconnection': 'bridgeStackConnection_id'}, {}], 'ocum.cifsshare': [{}, {}], 'ocum.clienteventdetails': [{'ocum.event': 'event_id'}, {}], 'ocum.event': [{'ocum.eventtypevalue': 'value_id'}, {'ocum.clienteventdetails': 'id', 'ocum.eventnote': 'id', 'ocum.eventontapsystemhealthalertmapping': 'id', 'ocum.trap': 'id'}], 'ocum.cluster': [{}, {'ocum.clusterhistorymonth': 'id', 'ocum.clusterhistoryweek': 'id', 'ocum.clusterhistoryyear': 'id', 'ocum.deferredmccresource': 'id', 'ocum.deferredontapalert': 'id', 'ocum.eventontapsystemhealthalertmapping': 'id', 'ocum.ocummonitoringstatus': 'id', 'ocum.ontapems': 'id', 'ocum.storagearrayclusterassociation': 'id', 'ocum.storagearrayportclusterassociation': 'id', 'ocum.trap': 'id'}], 'ocum.clusterhistorymonth': [{'ocum.cluster': 'clusterId'}, {}], 'ocum.clusterhistoryweek': [{'ocum.cluster': 'clusterId'}, {}], 'ocum.clusterhistoryyear': [{'ocum.cluster': 'clusterId'}, {}], 'ocum.clusternode': [{}, {'ocum.clusternodehistorymonth': 'id', 'ocum.clusternodehistoryweek': 'id', 'ocum.clusternodehistoryyear': 'id', 'ocum.externalcache': 'id', 'ocum.externalcachehistorymonth': 'id', 'ocum.externalcachehistoryweek': 'id', 'ocum.externalcachehistoryyear': 'id'}], 'ocum.clusternodehistorymonth': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.clusternodehistoryweek': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.clusternodehistoryyear': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.conditiongroup': [{'ocum.selectioncriterion': 'selectionCriterionId'}, {'ocum.conditiontable': 'id'}], 'ocum.selectioncriterion': [{'ocum.annotationrule': 'annotationRuleId', 'ocum.groupmembershiprule': 'groupMembershipRuleId'}, {'ocum.conditiongroup': 'id'}], 'ocum.conditiontable': [{'ocum.conditiongroup': 'conditionGroupId'}, {}], 'ocum.customeventtype': [{'ocum.eventtype': 'id'}, {}], 'ocum.eventtype': [{'ocum.eventtypecategorycontainer': 'parentCategory_id'}, {'ocum.customeventtype': 'id', 'ocum.eventtypecategoryclosureassociation': 'id', 'ocum.eventtypesourcetypes': 'id', 'ocum.eventtypevalue': 'id'}], 'ocum.customeventtypevalue': [{'ocum.eventtypevalue': 'id'}, {}], 'ocum.databaseproperty': [{}, {}], 'ocum.datapolicy': [{'ocum.vserver': 'vserver_id'}, {}], 'ocum.vserver': [{'ocum.volume': 'metadataVolumeId'}, {'ocum.datapolicy': 'id', 'ocum.storageservicevserverdestination': 'id', 'ocum.vserverhistorymonth': 'id', 'ocum.vserverhistoryweek': 'id', 'ocum.vserverhistoryyear': 'id'}], 'ocum.datasource': [{}, {}], 'ocum.deferredmccresource': [{'ocum.cluster': 'cluster_id'}, {}], 'ocum.deferredontapalert': [{'ocum.cluster': 'cluster_id'}, {}], 'ocum.deletedvolume': [{}, {}], 'ocum.diskaggregaterelationship': [{'ocum.aggregate': 'lastKnownAggregateId', 'ocum.wafldisk': 'lastKnownDiskId'}, {}], 'ocum.wafldisk': [{}, {'ocum.diskaggregaterelationship': 'id'}], 'ocum.efficiencypolicy': [{}, {}], 'ocum.eventnote': [{'ocum.event': 'event_id'}, {}], 'ocum.eventontapsystemhealthalertmapping': [{'ocum.cluster': 'alert_cluster_id', 'ocum.event': 'event_id'}, {}], 'ocum.eventtypecategorycontainer': [{}, {'ocum.eventtype': 'id', 'ocum.eventtypecategoryclosureassociation': 'id'}], 'ocum.eventtypecategoryclosureassociation': [{'ocum.eventtypecategorycontainer': 'container_id', 'ocum.eventtype': 'eventType_id'}, {}], 'ocum.eventtypesourcetypes': [{'ocum.eventtype': 'eventType_id'}, {}], 'ocum.exportpolicy': [{}, {}], 'ocum.exportrule': [{}, {}], 'ocum.externalcache': [{'ocum.clusternode': 'clusterNode_id'}, {}], 'ocum.externalcachehistorymonth': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.externalcachehistoryweek': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.externalcachehistoryyear': [{'ocum.clusternode': 'clusterNodeId'}, {}], 'ocum.favorite': [{}, {}], 'ocum.fcptarget': [{}, {}], 'ocum.flashcard': [{}, {}], 'ocum.groupaction': [{'ocum.groups': 'groupId'}, {'ocum.groupactionargument': 'id'}], 'ocum.groups': [{}, {'ocum.groupaction': 'id', 'ocum.groupmembership': 'id', 'ocum.groupmembershiprule': 'id'}], 'ocum.groupactionargument': [{'ocum.groupaction': 'groupActionId'}, {}], 'ocum.groupmembership': [{'ocum.groups': 'groupId', 'ocum.groupmembershiprule': 'groupMembershipRuleId'}, {}], 'ocum.groupmembershiprule': [{'ocum.groups': 'groupId'}, {'ocum.groupmembership': 'id', 'ocum.selectioncriterion': 'id'}], 'ocum.heartbeatclient': [{}, {'ocum.heartbeatservice': 'id'}], 'ocum.heartbeatservice': [{'ocum.heartbeatclient': 'heartbeatClient_id'}, {}], 'ocum.hibernate_sequences': [{}, {}], 'ocum.infinitevolhistorymonth': [{'ocum.volume': 'volumeId'}, {}], 'ocum.volume': [{'ocum.storageclass': 'systemStorageClass_id'}, {'ocum.infinitevolhistorymonth': 'id', 'ocum.infinitevolhistoryweek': 'id', 'ocum.infinitevolhistoryyear': 'id', 'ocum.storageservicenodemember': 'id', 'ocum.volumegrowthrateinfo': 'id', 'ocum.volumehistorymonth': 'id', 'ocum.volumehistoryweek': 'id', 'ocum.volumehistoryyear': 'id', 'ocum.volumejunctionpathhistory': 'id', 'ocum.volumeregressioninfo': 'id', 'ocum.vserver': 'id'}], 'ocum.infinitevolhistoryweek': [{'ocum.volume': 'volumeId'}, {}], 'ocum.infinitevolhistoryyear': [{'ocum.volume': 'volumeId'}, {}], 'ocum.initiator': [{}, {}], 'ocum.initiatorgroup': [{}, {}], 'ocum.internodeconnection': [{}, {'ocum.internodelink': 'id'}], 'ocum.internodelink': [{'ocum.internodeconnection': 'InterNodeConnection_id'}, {}], 'ocum.interswitchconnection': [{'ocum.switch': 'secondSwitch_id'}, {'ocum.interswitchlink': 'id', 'ocum.switchinterswitchrelationship': 'id'}], 'ocum.switch': [{'ocum.switch': 'secondSwitch_id'}, {'ocum.interswitchconnection': 'id', 'ocum.nodeswitchconnection': 'id', 'ocum.switchbridgeconnection': 'id', 'ocum.switchinterswitchrelationship': 'id'}], 'ocum.interswitchlink': [{'ocum.interswitchconnection': 'interSwitchConnection_id'}, {}], 'ocum.job': [{}, {'ocum.task': 'id', 'ocum.taskretry': 'id'}], 'ocum.ldapserver': [{}, {}], 'ocum.logicalinterface': [{}, {}], 'ocum.lun': [{}, {}], 'ocum.managementstation': [{}, {}], 'ocum.metroclusterrelationship': [{}, {}], 'ocum.networkport': [{}, {}], 'ocum.nodebridgeconnection': [{'ocum.bridge': 'bridge_id'}, {'ocum.nodebridgelink': 'id'}], 'ocum.nodebridgelink': [{'ocum.nodebridgeconnection': 'nodeBridgeConnection_id'}, {}], 'ocum.nodestackconnection': [{}, {'ocum.nodestacklink': 'id'}], 'ocum.nodestacklink': [{'ocum.nodestackconnection': 'nodeStackConnection_id'}, {}], 'ocum.nodeswitchconnection': [{'ocum.switch': 'switch_id'}, {'ocum.nodeswitchlink': 'id'}], 'ocum.nodeswitchlink': [{'ocum.nodeswitchconnection': 'nodeSwitchConnection_id'}, {}], 'ocum.ocummonitoringstatus': [{'ocum.cluster': 'cluster_id'}, {}], 'ocum.ontapalert': [{}, {}], 'ocum.ontapems': [{'ocum.cluster': 'cluster_id'}, {'ocum.ontapemsparameter': 'id'}], 'ocum.ontapemsparameter': [{'ocum.ontapems': 'ontapEms_id'}, {}], 'ocum.ontapfaultinfo': [{}, {}], 'ocum.optionchainvalue': [{}, {}], 'ocum.persistentproperty': [{}, {}], 'ocum.plex': [{}, {}], 'ocum.portset': [{}, {}], 'ocum.qrtz_blob_triggers': [{}, {}],  'ocum.qrtz_calendars': [{}, {}], 'ocum.qrtz_cron_triggers': [{}, {}], 'ocum.qrtz_fired_triggers': [{}, {}], 'ocum.qrtz_locks': [{}, {}], 'ocum.qrtz_paused_trigger_grps': [{}, {}], 'ocum.qrtz_scheduler_state': [{}, {}], 'ocum.qrtz_simple_triggers': [{}, {}], 'ocum.qrtz_simprop_triggers': [{}, {}], 'ocum.qtree': [{}, {}], 'ocum.readytaskworkitemqueueentry': [{}, {}], 'ocum.report': [{}, {'ocum.reportschedulerelationship': 'id'}], 'ocum.reportschedule': [{}, {'ocum.reportschedulerelationship': 'id'}], 'ocum.reportschedulerelationship': [{'ocum.reportschedule': 'reportSchedule_id', 'ocum.report': 'report_id'}, {}], 'ocum.resourcepool': [{}, {'ocum.resourcepoolaggregates': 'id', 'ocum.storageservicenoderesourcepool': 'id'}], 'ocum.resourcepoolaggregates': [{'ocum.aggregate': 'aggregate_id', 'ocum.resourcepool': 'resourcePool_id'}, {}], 'ocum.ruletemplate': [{}, {}], 'ocum.serviceworkflow': [{}, {'ocum.storageservicenode': 'id'}], 'ocum.snapmirrorrelationship': [{}, {'ocum.snapmirrortransfer': 'id', 'ocum.storageserviceconnectionmember': 'id'}], 'ocum.snapmirrortransfer': [{'ocum.snapmirrorrelationship': 'snapMirrorRelationshipId'}, {}], 'ocum.snapshotexpirerecord': [{}, {}], 'ocum.snapshotmetadata': [{}, {}], 'ocum.snapshotpolicy': [{}, {}], 'ocum.storagearray': [{}, {'ocum.storagearrayclusterassociation': 'id', 'ocum.storagearrayport': 'id'}], 'ocum.storagearrayclusterassociation': [{'ocum.cluster': 'cluster_id', 'ocum.storagearray': 'storageArray_id'}, {}], 'ocum.storagearraylunpath': [{'ocum.storagearrayport': 'storageArrayPort_id'}, {}], 'ocum.storagearrayport': [{'ocum.storagearray': 'storageArray_id'}, {'ocum.storagearraylunpath': 'id', 'ocum.storagearrayportclusterassociation': 'id'}], 'ocum.storagearrayportclusterassociation': [{'ocum.cluster': 'cluster_id', 'ocum.storagearrayport': 'storageArrayPort_id'}, {}], 'ocum.storageclass': [{}, {'ocum.volume': 'id'}], 'ocum.storageservice': [{}, {'ocum.storageservice_contacts': 'id', 'ocum.storageserviceconnection': 'id', 'ocum.storageservicenode': 'id', 'ocum.storageservicerootmemberinfo': 'id', 'ocum.storageservicesubscription': 'id'}], 'ocum.storageservice_contacts': [{'ocum.storageservice': 'storageService_id'}, {}], 'ocum.storageserviceconnection': [{'ocum.storageservicenode': 'sourceNode_id', 'ocum.storageservice': 'storageService_id'}, {'ocum.storageserviceconnectionmember': 'id'}], 'ocum.storageservicenode': [{'ocum.storageservicenode': 'sourceNode_id', 'ocum.serviceworkflow': 'serviceWorkflow_id', 'ocum.storageservice': 'storageService_id'}, {'ocum.storageserviceconnection': 'id', 'ocum.storageservicenodemember': 'id', 'ocum.storageservicenoderesourcepool': 'id'}], 'ocum.storageserviceconnectionmember': [{'ocum.storageserviceconnection': 'connection_id', 'ocum.storageservicenodemember': 'sourceNodeMember_id', 'ocum.snapmirrorrelationship': 'relationship_id', 'ocum.storageservicerootmemberinfo': 'rootMemberInfo_id'}, {}], 'ocum.storageservicenodemember': [{'ocum.snapmirrorrelationship': 'relationship_id', 'ocum.storageservicenode': 'node_id', 'ocum.storageservicerootmemberinfo': 'rootMemberInfo_id', 'ocum.volume': 'volume_id'}, {'ocum.storageserviceconnectionmember': 'id', 'ocum.storageservicerootmemberinfo': 'id'}], 'ocum.storageservicerootmemberinfo': [{'ocum.storageservicenodemember': 'rootNodeMember_id', 'ocum.storageservice': 'storageService_id'}, {'ocum.storageserviceconnectionmember': 'id', 'ocum.storageservicenodemember': 'id', 'ocum.storageservicesubscriptionrootmember': 'id'}], 'ocum.storageservicenoderesourcepool': [{'ocum.resourcepool': 'resourcePool_id', 'ocum.storageservicenode': 'storageServiceNode_id'}, {}], 'ocum.storageservicesubscription': [{'ocum.storageservice': 'storageService_id'}, {'ocum.storageservicesubscription_metadatafields': 'id', 'ocum.storageservicesubscriptionrootmember': 'id'}], 'ocum.storageservicesubscription_metadatafields': [{'ocum.storageservicesubscription': 'StorageServiceSubscription_id'}, {}], 'ocum.storageservicesubscriptionrootmember': [{'ocum.storageservicerootmemberinfo': 'rootMemberInfo_id', 'ocum.storageservicesubscription': 'subscription_id'}, {}], 'ocum.storageservicevserverdestination': [{'ocum.vserver': 'sourceVserver_id'}, {}], 'ocum.storageshelf': [{}, {}], 'ocum.subscribedems': [{}, {}], 'ocum.switchbridgeconnection': [{'ocum.bridge': 'bridge_id', 'ocum.switch': 'switch_id'}, {'ocum.switchbridgelink': 'id'}], 'ocum.switchbridgelink': [{'ocum.switchbridgeconnection': 'switchBridgeConnection_id'}, {}], 'ocum.switchinterswitchrelationship': [{'ocum.interswitchconnection': 'interSwitchConnection_id', 'ocum.switch': 'switch_id'}, {}], 'ocum.targetportalgroup': [{}, {}], 'ocum.task': [{'ocum.job': 'job_id'}, {'ocum.taskmessage': 'id', 'ocum.taskobjectinteraction': 'id', 'ocum.taskpredecessor': 'id', 'ocum.taskretry': 'id', 'ocum.taskstatuschange': 'id'}], 'ocum.taskmessage': [{'ocum.task': 'task_id'}, {}], 'ocum.taskobjectinteraction': [{'ocum.task': 'task_id'}, {}], 'ocum.taskpredecessor': [{'ocum.task': 'task_id'}, {}], 'ocum.taskretry': [{'ocum.job': 'job_id', 'ocum.task': 'task_id'}, {}], 'ocum.taskstatuschange': [{'ocum.task': 'task_id'}, {}], 'ocum.thresholdobjectstocheck': [{}, {}], 'ocum.trap': [{'ocum.event': 'event_id', 'ocum.cluster': 'source_id'}, {'ocum.trapvarbinding': 'id'}], 'ocum.trapvarbinding': [{'ocum.trap': 'trap_id'}, {}], 'ocum.userquota': [{}, {}], 'ocum.volumegrowthrateinfo': [{'ocum.volume': 'volume_id'}, {}], 'ocum.volumehistorymonth': [{'ocum.volume': 'volumeId'}, {}], 'ocum.volumehistoryweek': [{'ocum.volume': 'volumeId'}, {}], 'ocum.volumehistoryyear': [{'ocum.volume': 'volumeId'}, {}], 'ocum.volumejunctionpathhistory': [{'ocum.volume': 'volume_id'}, {}], 'ocum.volumemovehistory': [{}, {}], 'ocum.volumeregressioninfo': [{'ocum.volume': 'volume_id'}, {}], 'ocum.volumesnapshot_metadatafields': [{}, {}], 'ocum.vserverhistorymonth': [{'ocum.vserver': 'vserverId'}, {}], 'ocum.vserverhistoryweek': [{'ocum.vserver': 'vserverId'}, {}], 'ocum.vserverhistoryyear': [{'ocum.vserver': 'vserverId'}, {}], 'sanscreen.implicit_commit': [{}, {}], 'sanscreen.user': [{}, {}], 'sanscreen.user_role': [{}, {}], 'scrub.dictionary': [{}, {}], 'scrub.patterns': [{}, {}]}

for l in list_track:
    db=l.split(".")[0]
    table=l.split(".")[1]
    #print(db)
    #print(l)
    connect(db,table,l,**parent_child)

fp.close()







