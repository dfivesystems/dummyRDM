ACNheader = b'\x41\x53\x43\x2d\x45\x31\x2e\x31\x37\x00\x00\x00'

vector_root_llrp = b'\x00\x00\x00\x0A'
vector_root_rpt = b'\x00\x00\x00\x05'
vector_root_broker = b'\x00\x00\x00\x09'
vector_root_ept = b'\x00\x00\x00\x0B'

vector_llrp_probe_request = b'\x00\x00\x00\x01'
vector_llrp_probe_reply = b'\x00\x00\x00\x02'
vector_llrp_rdm_cmd = b'\x00\x00\x00\x03'
vector_probe_request_data = b'\x01'
vector_probe_reply_data = b'\x01'

vector_broker_connect = b'\x00\x01'
vector_broker_connect_reply = b'\x00\x02'
vector_broker_client_entry_update = b'\x00\x03'
vector_broker_redirect_v4 = b'\x00\x04'
vector_broker_redirect_v6 = b'\x00\x05'
vector_broker_fetch_client_list = b'\x00\x06'
vector_broker_connected_client_list = b'\x00\x07'
vector_broker_client_add = b'\x00\x08'
vector_broker_client_remove = b'\x00\x09'
vector_broker_client_entry_change = b'\x00\x0A'
vector_broker_request_dynamic_uids = b'\x00\x0B'
vector_broker_assigned_dynamic_uids = b'\x00\x0C'
vector_broker_fetch_dynamic_uid_list = b'\x00\x0D'
vector_broker_disconnect = b'\x00\x0E'
vector_broker_null = b'\x00\x0F'

vector_rpt_request = b'\x00\x00\x00\x01'
vector_rpt_status = b'\x00\x00\x00\x02'
vector_rpt_notification = b'\x00\x00\x00\x03'

vector_request_rdm_cmd = b'\x01'

vector_rpt_status_unknown_rpt_uid = b'\x00\x01'
vector_rpt_status_rdm_timeout = b'\x00\x02'
vector_rpt_status_rdm_invalid_response = b'\x00\x03'
vector_rpt_status_unknown_rdm_uid = b'\x00\x04'
vector_rpt_unknown_endpoint = b'\x00\x05'
vector_rpt_status_broadcast_complete = b'\x00\x06'
vector_rpt_status_unknown_vector = b'\x00\x07'
vector_rpt_status_invalid_message = b'\x00\x08'
vector_rpt_status_invalid_command_class = b'\x00\x09'

vector_notification_rdm_cmd = b'\x01'

vector_rdm_cmd_rdm_data = b'\xCC'

vector_ept_data = b'\x00\x00\x00\x01'
vector_ept_status = b'\x00\x00\x00\x02'

vector_ept_status_unknown_cid = b'\x00\x01'
vector_ept_status_unknown_vector = b'\x00\x02'