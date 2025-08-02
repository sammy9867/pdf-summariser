import { createServer, Model, Factory, Response } from 'miragejs';
import { faker } from '@faker-js/faker';

export const server = createServer({
  environment: 'test',

  models: {
    document: Model,
  },

  factories: {
    document: Factory.extend({
      created() {
        return faker.date.recent().toISOString();
      },
      modified() {
        return faker.date.recent().toISOString();
      },
      uploaded_file() {
        return {
          name: faker.system.fileName({ extension: 'pdf' }),
          file: faker.system.filePath(),
          size: faker.number.int({ min: 1024, max: 10485760 }),
          created: faker.date.recent().toISOString(),
          modified: faker.date.recent().toISOString(),
        };
      },
      uuid() {
        return faker.string.uuid();
      },
    }),
  },

  routes() {
    this.namespace = 'api/v1';
    this.urlPrefix = 'http://localhost:8000';

    this.get('/documents', (schema) => {
      return schema.documents.all().models.map((model: any) => model.attrs);
    });

    this.post('/documents/upload', (schema, request) => {
      const documentData = {
        created: faker.date.recent().toISOString(),
        modified: faker.date.recent().toISOString(),
        uploaded_file: {
          name: faker.system.fileName({ extension: 'pdf' }),
          file: faker.system.filePath(),
          size: faker.number.int({ min: 1024, max: 10485760 }),
          created: faker.date.recent().toISOString(),
          modified: faker.date.recent().toISOString(),
        },
        uuid: faker.string.uuid(),
      };

      const document = schema.documents.create(documentData);
      return document.attrs;
    });

    this.get('/documents/:id/stream', () => {
      return new Response(200, {}, 'SSE endpoint');
    });
  },
});
