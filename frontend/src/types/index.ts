export interface UploadedFile {
    created: string;
    file: string;
    modified: string;
    name: string;
    size: number;
}

export interface Document {
    created: string;
    modified: string;
    session_id: string;
    uploaded_file: UploadedFile;
    uuid: string;
}

export interface SSEMessage {
    type: string;
    data: string;
}
