# PharmaShield — SAP BTP / ABAP RAP Service Setup & Eclipse ADT Guide

This guide details how to import, compile, activate, and publish the PharmaShield OData V4 Web API Service Binding on SAP BTP / SAP S/4HANA using Eclipse ADT.

---

## 1. Generated SAP Artifacts

| SAP Layer | File Location in Repository | Object Name in SAP |
| :--- | :--- | :--- |
| **Transparent Table** | [`sap/table/zpharmashield_shp.tabl.asddl`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/table/zpharmashield_shp.tabl.asddl) | `ZPHARMASHIELD_SHP` |
| **CDS Data Model** | [`sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls) | `ZI_PHARMASHIELD_SHIPMENT` |
| **ABAP Governance Engine** | [`sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap) | `ZCL_PHARMASHIELD_GOVERNANCE` |
| **RAP Behavior Def** | [`sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef) | `ZC_PHARMASHIELD_SHIPMENT` |
| **RAP Behavior Class** | [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap) | `ZBP_I_PHARMASHIELD_SHIPMENT` |
| **RAP Behavior Locals** | [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap) | `LHC_SHIPMENT` |
| **Service Definition** | [`sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv) | `ZUI_PHARMASHIELD_GOV` |
| **OData V4 Binding** | [`sap/binding/ZUI_PHARMASHIELD_GOV_O4.srvb.xml`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/binding/ZUI_PHARMASHIELD_GOV_O4.srvb.xml) | `ZUI_PHARMASHIELD_GOV_O4` |

---

## 2. Steps to Activate & Publish in Eclipse ADT

1. **Open Eclipse ADT** and log in to your ABAP Project (SAP BTP ABAP Environment or SAP S/4HANA).
2. Create package `$PHARMASHIELD` or select your package.
3. Import/Create the objects in order:
   - **Step 1:** Create Database Table `ZPHARMASHIELD_SHP` and paste contents of [`sap/table/zpharmashield_shp.tabl.asddl`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/table/zpharmashield_shp.tabl.asddl). Press `Ctrl+F3` to Activate.
   - **Step 2:** Create Data Definition `ZI_PHARMASHIELD_SHIPMENT` and paste contents of [`sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls). Press `Ctrl+F3` to Activate.
   - **Step 3:** Create ABAP Class `ZCL_PHARMASHIELD_GOVERNANCE` and paste contents of [`sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap). Press `Ctrl+F3` to Activate.
   - **Step 4:** Create Behavior Definition `ZC_PHARMASHIELD_SHIPMENT` and paste contents of [`sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef). Press `Ctrl+F3` to Activate.
   - **Step 5:** Create ABAP Behavior Class `ZBP_I_PHARMASHIELD_SHIPMENT`, paste [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap) in Global tab and [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap) in Local Definitions/Implementations tab. Press `Ctrl+F3` to Activate.
   - **Step 6:** Create Service Definition `ZUI_PHARMASHIELD_GOV` and paste contents of [`sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv). Press `Ctrl+F3` to Activate.
   - **Step 7:** Create Service Binding `ZUI_PHARMASHIELD_GOV_O4` (Binding Type: **OData V4 - Web API**). Press `Ctrl+F3` to Activate.
4. Click **Publish** button on the Service Binding editor window.

---

## 3. Where to Find the Published OData V4 Service URL

After clicking **Publish** in Eclipse ADT:
1. In the Service Binding editor window under **Service URL / Entity Sets**, locate the published endpoint URL.
2. It will look like:
   `https://<your-sap-btp-system>.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001`
