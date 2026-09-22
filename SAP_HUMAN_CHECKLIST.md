# PharmaShield — SAP BTP / Eclipse ADT Human Action Checklist

This checklist contains **ONLY** the actions required to be performed manually within **Eclipse ADT (ABAP Development Tools)** and the **SAP BTP Cockpit**.

---

### Prerequisites
- Eclipse IDE with **ABAP Development Tools (ADT)** plugin installed.
- Logged into your SAP BTP ABAP Environment Project (e.g. `$PHARMASHIELD` or your active development package).

---

### Step 1: Create and Activate Transparent Database Table
* **WHERE**: Eclipse ADT -> Project Explorer -> Your ABAP Package (e.g., `ZPHARMASHIELD`) -> Right-click `Dictionary` -> **New Database Table**.
* **WHAT TO ENTER**:
  * Name: `ZPHARMASHIELD_SHP`
  * Description: `PharmaShield Cold Chain Shipment Persistent Table`
  * Source Code: Copy and paste the complete content of [`sap/table/zpharmashield_shp.tabl.asddl`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/table/zpharmashield_shp.tabl.asddl).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **EXPECTED RESULT**: Table `ZPHARMASHIELD_SHP` is activated with status **Active**.

---

### Step 2: Create and Activate CDS Data Model Root View Entity
* **WHERE**: Eclipse ADT -> Right-click `Core Data Services` -> **New Data Definition**.
* **WHAT TO ENTER**:
  * Name: `ZI_PHARMASHIELD_SHIPMENT`
  * Description: `PharmaShield Cold Chain Shipment CDS Data Model`
  * Referenced Table: `zpharmashield_shp`
  * Source Code: Copy and paste the complete content of [`sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/cds/ZI_PHARMASHIELD_SHIPMENT.ddls.asddls).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **EXPECTED RESULT**: CDS Root View Entity `ZI_PHARMASHIELD_SHIPMENT` is activated with status **Active**.

---

### Step 3: Create and Activate ABAP Governance Rules Engine Class
* **WHERE**: Eclipse ADT -> Right-click `Source Code Library` -> **New ABAP Class**.
* **WHAT TO ENTER**:
  * Name: `ZCL_PHARMASHIELD_GOVERNANCE`
  * Description: `PharmaShield Cold Chain ABAP Governance Engine`
  * Source Code: Copy and paste the complete content of [`sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZCL_PHARMASHIELD_GOVERNANCE.clas.abap).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **EXPECTED RESULT**: Class `ZCL_PHARMASHIELD_GOVERNANCE` is activated with status **Active**.

---

### Step 4: Create and Activate RAP Behavior Definition & Implementation
* **WHERE**: Eclipse ADT -> Right-click `Core Data Services` -> **New Behavior Definition**.
* **WHAT TO ENTER**:
  * Name: `ZI_PHARMASHIELD_SHIPMENT` (or `ZC_PHARMASHIELD_SHIPMENT`)
  * Implementation Type: `Managed`
  * Behavior Definition Source Code: Copy and paste the content of [`sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/rap/ZC_PHARMASHIELD_SHIPMENT.bdef.asbdef).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **BEHAVIOR IMPLEMENTATION CLASS**:
  * Create ABAP Class `ZBP_I_PHARMASHIELD_SHIPMENT`.
  * In the **Global Class** tab, paste [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.abap).
  * In the **Local Types** (`Local Definitions / Implementations`) tab, paste [`sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/abap/ZBP_I_PHARMASHIELD_SHIPMENT.clas.locals_imp.abap).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **EXPECTED RESULT**: RAP Behavior Definition and Implementation are both activated with status **Active**.

---

### Step 5: Create and Activate Service Definition
* **WHERE**: Eclipse ADT -> Right-click `Business Services` -> **New Service Definition**.
* **WHAT TO ENTER**:
  * Name: `ZUI_PHARMASHIELD_GOV`
  * Description: `PharmaShield Cold Chain Governance Service Definition`
  * Source Code: Copy and paste the content of [`sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv`](file:///Users/siddharthsati/Desktop/PHARAMA%20SHIELD%20/sap/srv/ZUI_PHARMASHIELD_GOV.srvd.srvdsrv).
* **WHAT TO CLICK**: Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
* **EXPECTED RESULT**: Service Definition `ZUI_PHARMASHIELD_GOV` is activated.

---

### Step 6: Create, Activate, and Publish OData V4 Service Binding
* **WHERE**: Eclipse ADT -> Right-click `Business Services` -> **New Service Binding**.
* **WHAT TO ENTER**:
  * Name: `ZUI_PHARMASHIELD_GOV_O4`
  * Description: `PharmaShield Cold Chain OData V4 Web API Binding`
  * Binding Type: `OData V4 - Web API`
  * Service Definition: `ZUI_PHARMASHIELD_GOV`
* **WHAT TO CLICK**:
  1. Click **Activate** (`Ctrl+F3` / `Cmd+F3`).
  2. In the Service Binding editor, click the **Publish** button.
* **EXPECTED RESULT**: Service is published. Under **Service URL / Entity Sets**, the published endpoint URL appears (e.g. `https://<tenant>.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001`).

---

### Step 7: Configure Environment Variables in `.env`
* **WHERE**: PharmaShield project root `.env` file.
* **WHAT TO ENTER**:
  ```env
  SAP_MODE=REAL
  SAP_ODATA_URL=https://<your-published-service-url>
  SAP_TOKEN_URL=https://<your-btp-subdomain>.authentication.eu10.hana.ondemand.com/oauth/token
  SAP_CLIENT_ID=<your-service-key-client-id>
  SAP_CLIENT_SECRET=<your-service-key-client-secret>
  ```
* **EXPECTED RESULT**: PharmaShield FastAPI connects live to your SAP BTP ABAP system.
