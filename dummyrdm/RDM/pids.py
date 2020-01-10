RDM_disc_unique_branch = 0x0001
RDM_disc_mute = 0x0002
RDM_disc_unmute = 0x0003
RDM_proxied_devices = 0x0010
RDM_proxied_device_count = 0x0011
RDM_comms_status = 0x0015

RDM_queued_messages = 0x0020
RDM_status_messages = 0x0030
RDM_status_id_description = 0x0031
RDM_clear_status_id = 0x0032
RDM_sub_device_status_report_threshold = 0x0033

RDM_supported_parameters = 0x0050
RDM_parameter_description = 0x0051

RDM_device_info = 0x0060
RDM_product_detail_id_list = 0x0070
RDM_device_model_description = 0x0080
RDM_manufacturer_label = 0x0081
RDM_device_label = 0x0082
RDM_factory_defaults = 0x0090
RDM_language_capabilities = 0x00A0
RDM_language = 0x00B0
RDM_software_version_label = 0x00C0
RDM_boot_software_version_id = 0x00C1
RDM_boot_software_version_label = 0x00C2

RDM_dmx_personality = 0x00E0
RDM_dmx_personality_description = 0x00E1
RDM_dmx_start_address = 0x00F0
RDM_dmx_slot_info = 0x0120
RDM_dmx_slot_description = 0x0121
RDM_dmx_default_slot_value = 0x0122

RDM_sensor_definition = 0x0200
RDM_sensor_value = 0x0201
RDM_record_sensors = 0x202

RDM_device_hours = 0x0400
RDM_lamp_hours = 0x0401
RDM_lamp_strikes = 0x0402
RDM_lamp_state = 0x0403
RDM_lamp_on_mode = 0x0404
RDM_device_power_cycles = 0x0405

RDM_display_invert = 0x0500
RDM_display_level = 0x0501

RDM_pan_invert = 0x0600
RDM_tilt_invert = 0x0601
RDM_pan_tilt_swap = 0x0602
RDM_real_time_clock = 0x0603

RDM_identify = 0x1000
RDM_reset_device = 0x1001
RDM_power_state = 0x1010
RDM_perform_selftest = 0x1020
RDM_selftest_description = 0x1021
RDM_capture_preset = 0x1030
RDM_preset_playback = 0x1031

#E1.37-1 PIDS
RDM_1371_DMX_block_address = 0x0140
RDM_1371_DMX_fail_mode = 0x0141
RDM_1371_DMX_startup_mode = 0x0142

RDM_1371_dimmer_info = 0x0340
RDM_1371_minimum_level = 0x0341
RDM_1371_maximum_level = 0x0342
RDM_1371_curve = 0x0343
RDM_1371_curve_description = 0x0344
RDM_1371_output_response_time = 0x0345
RDM_1371_output_response_time_description = 0x0346
RDM_1371_modulation_frequency = 0x0347
RDM_1371_modulation_frequency_description = 0x0348

RDM_1371_burn_in = 0x0440

RDM_1371_lock_pin = 0x0640
RDM_1371_lock_state = 0x0641
RDM_1371_lock_state_description = 0x0642

RDM_1371_identify_mode = 0x1040
RDM_1371_preset_info = 0x1041
RDM_1371_preset_status = 0x1042
RDM_1371_preset_mergemode = 0x1043
RDM_1371_poweron_selftest = 0x1044

#E1.37-2 PIDS
RDM_1372_list_interfaces = 0x0700
RDM_1372_interface_label = 0x0701
RDM_1372_interface_hardware_address = 0x0702
RDM_1372_interface_ipv4_dhcp_mode = 0x0703
RDM_1372_interface_ipv4_zeroconf_mode = 0x0704
RDM_1372_interface_ipv4_current_address = 0x0705
RDM_1372_interface_ipv4_static_address = 0x0706
RDM_1372_interface_renew_dhcp = 0x0707
RDM_1372_interface_release_dhcp = 0x0708
RDM_1372_interface_apply_configuration = 0x0709
RDM_1372_ipv4_default_route = 0x070A
RDM_1372_dns_ipv4_name_server = 0x070B
RDM_1372_dns_hostname = 0x070C
RDM_1372_dns_domain_name = 0x070D

#E1.33 PIDS
E133_component_scope = 0x0800
E133_search_domain = 0x0801
E133_tcp_comms_status = 0x0802
E133_broker_status = 0x0803
