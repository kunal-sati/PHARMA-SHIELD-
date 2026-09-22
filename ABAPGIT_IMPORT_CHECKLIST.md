# PharmaShield — abapGit Automated Import & Activation Checklist

This repository is fully configured for **abapGit** and **ABAP for Cloud Development (Language Version 5)** for **SAP BTP ABAP Environment / SAP S/4HANA Cloud**.

By using abapGit with the dedicated repository, all Database Tables, CDS Views, RAP Behavior Definitions, ABAP Classes, and Service Definitions are **imported and activated automatically** in SAP BTP, eliminating manual code creation.

---

### Step 1: Clone and Pull via abapGit in Eclipse ADT
* **WHERE**: Eclipse ADT -> Open View **abapGit Repositories** (`Window` -> `Show View` -> `Other...` -> search `abapGit`).
* **WHAT TO CLICK**: Click the **+** (Clone Repository / Link Repository) button.
* **WHAT TO ENTER**:
  * Git Repository URL: `https://github.com/kunal-sati/pharmashield-abap.git`
  * Package: `ZPHARMASHIELD` (or `$PHARMASHIELD`)
  * Folder Logic: `Prefix` (configured in `.abapgit.xml`)
* **WHAT TO CLICK**: Click **Pull / Import All Objects**.
* **EXPECTED RESULT**: All 8 ABAP Cloud objects are pulled, created, and activated in SAP BTP:
  1. `TABL` `ZPHARMASHIELD_SHP` (Persistent Database Table)
  2. `DDLS` `ZI_PHARMASHIELD_SHIPMENT` (CDS Root View Entity)
  3. `CLAS` `ZCL_PHARMASHIELD_GOVERNANCE` (ABAP Governance Rules Engine)
  4. `BDEF` `ZI_PHARMASHIELD_SHIPMENT` (RAP Behavior Definition)
  5. `CLAS` `ZBP_I_PHARMASHIELD_SHIPMENT` (RAP Behavior Implementation Class)
  6. `SRVD` `ZUI_PHARMASHIELD_GOV` (Governance Service Definition)
  7. `SRVB` `ZUI_PHARMASHIELD_GOV_O4` (OData V4 Web API Service Binding)
  8. `DEVC` `ZPHARMASHIELD` (Package definition)

---

### Step 2: Publish the OData V4 Service Binding (Only Unavoidable GUI Step)
* **WHERE**: Eclipse ADT -> Project Explorer -> Package `ZPHARMASHIELD` -> `Business Services` -> `Service Bindings` -> Open `ZUI_PHARMASHIELD_GOV_O4`.
* **WHAT TO CLICK**: Click the **Publish** button in the Service Binding editor.
* **EXPECTED RESULT**: The service is published with status **Published**. Under **Service URL / Entity Sets**, copy the published service URL.

---

### Step 3: Configure Endpoint in `.env`
* **WHERE**: Project root `.env` file.
* **WHAT TO ENTER**:
  ```env
  SAP_MODE=REAL
  SAP_ODATA_URL=https://<your-btp-system>.s4hana.ondemand.com/sap/opu/odata4/sap/zui_pharmashield_gov_o4/srvd/sap/zui_pharmashield/0001
  SAP_TOKEN_URL=https://<your-btp-subdomain>.authentication.eu10.hana.ondemand.com/oauth/token
  SAP_CLIENT_ID=<your-service-key-client-id>
  SAP_CLIENT_SECRET=<your-service-key-client-secret>
  ```
* **EXPECTED RESULT**: PharmaShield FastAPI backend communicates live with your SAP BTP ABAP RAP service.
