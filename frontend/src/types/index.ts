export interface UploadedFile {
  created: string;
  modified: string;
  name: string;
  size: number;
  uuid: string;
}

export interface Document {
  created: string;
  modified: string;
  uploaded_file: UploadedFile;
  uuid: string;
}

export interface SSEMessage {
  type: string;
  data: string;
}
