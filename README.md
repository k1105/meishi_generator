```mermaid
%%{init: {'theme': 'default', 'flowchart': { 'curve': 'linear', 'nodeSpacing': 50, 'rankSpacing': 50 }}}%%
flowchart TD

    %% Style definitions
    classDef user fill:#E0F7FA,stroke:#006064,stroke-width:2px;
    classDef dev fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef api fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef external fill:#ECEFF1,stroke:#455A64,stroke-width:1.5px;
    classDef highlight fill:#FFEBEE,stroke:#C62828,stroke-width:3px;

    %% Actors
    User[User]:::user
    Dev[Developer]:::dev

    %% Local environment
    subgraph UserPC_LocalEnvironment["User PC (Local Execution)"]
        UI[Front End (Next.js)]:::highlight
        API[Back End (Python + Node.js)]:::highlight
        PDFGen[PDF Generator (pdfkit)]:::highlight
        DropUpload[Dropbox Upload Module]:::highlight
    end

    %% External API
    subgraph ExternalAPI["External API (via HTTPS)"]
        OpenAI[OpenAI API (Design, Analysis)]:::external
        Dropbox[Dropbox API (Storage)]:::external
    end

    %% Access flows
    User -->|Launch and input| UI
    UI -->|Send data| API
    API -->|Request PDF| PDFGen
    PDFGen -->|Return PDF| API
    API -->|Upload PDF| DropUpload
    DropUpload -->|HTTPS| Dropbox
    API -->|Use API| OpenAI

    %% Developer flows
    Dev -->|Edit front end| UI
    Dev -->|Modify backend| API

    %% Legend
    subgraph Legend["Legend"]
        L1[Development Scope]:::highlight
        L2[User]:::user
        L3[Developer]:::dev
        L4[External API (HTTPS)]:::external
    end
```
