import subprocess
import os
import util
import apps.cds.syn as syn1
import apps.cds.floorplan as fp1
import apps.cds.pdn as pdn1
import apps.cds.place as place1
import apps.cds.cts as cts1
import apps.cds.route as route1
import apps.cds.drc as drc1
import apps.opensource.syn.yosys as syn2

def run(design, flow):
    design_name = design.top_name
    run_path = util.getRunPath(design, "Cadence")
    print(run_path)
    make_file = open(run_path + "/" + "Makefile", "w")
    tcl_path = util.getScriptPath(design, "Cadence")
    overall_tcl = open(tcl_path + "/" + "flow.tcl", 'w', encoding='utf-8')
    for x_list in flow.ops:
        x = x_list[0]
        if x[0] == "GenusSynth":
            script_path = "../scripts/"
            tmp_op_syn = eval("syn1." + "GenusSynth" + "(design)")
            for param in flow.params_syn:
                tmp_op_syn.setParams(param[0], param[1])
            tmp_op_syn.config(design, design_name + "_" + x[1])
            make_file.write("all:\n")
            make_file.write("\tgenus -legacy_ui -batch -files " + script_path + design_name + "_" + x[1] + ".tcl\n")

        if x[0] == "YosysSynth":
            script_path = "../scripts/"
            tmp_op_syn = eval("syn2." + "YosysSynth" + "(design)")
            tmp_op_syn.config(design, design_name + "_" + x[1])
            make_file.write("all:\n")
            make_file.write("\tyosys " + script_path + design_name + "_" + x[1] + ".ys\n")

        if x[0] == "InnovusFloorplan":
            tmp_op_fp = eval("fp1." + "InnovusFloorplan" + "(design)")
            for y in flow.params_fp:
                tmp_op_fp.setParams(y[0], y[1])
            tmp_op_fp.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_floorplan.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPDN":
            tmp_op_pdn = eval("pdn1." + "InnovusPDN" + "(design)")
            tmp_op_pdn.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_pdn.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusPlace":
            tmp_op_place = eval("place1." + "InnovusPlace" + "(design)")
            for param in flow.params_place:
                if param[1] == True:
                    tmp_op_place.setParams(param[0])
            tmp_op_place.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_place.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusCTS":
            tmp_op_cts = eval("cts1." + "InnovusCTS" + "(design)")
            tmp_op_cts.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_cts.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusRoute":
            tmp_op_route = eval("route1." + "InnovusRoute" + "(design)")
            for param in flow.params_route:
                tmp_op_route.setParams(param[0], param[1])
            tmp_op_route.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_route.tcl\n'%(tcl_path, design_name))

        if x[0] == "InnovusDRC":
            tmp_op_drc = eval("drc1." + "InnovusDRC" + "(design)")
            tmp_op_drc.config(design, design_name + "_" + x[1])
            overall_tcl.write('source %s/%s_to_drc.tcl\n'%(tcl_path, design_name))
    

    #make_file.write("\tinnovus -batch -files " + script_path + "flow.tcl")
    run_path = util.getRunPath(design, "Yosys")
    os.chdir(run_path)
    print(os.getcwd())
    #cmd_clean = 'rm innovus.* genus.*'
    #subprocess.Popen(cmd_clean, shell=True).wait()
    #cmd_clean = 'rm -rf fv'
    #subprocess.Popen(cmd_clean, shell=True).wait()
    cmd = 'make'
    #subprocess.Popen(cmd)
    subprocess.Popen(cmd, shell=True).wait()

    return design

