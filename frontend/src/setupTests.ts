import '@testing-library/jest-dom';
import { server } from './tests/__mocks__/server';

beforeEach(() => {
  if (server.db) {
    server.db.emptyData();
    server.createList('document', 2);
  }
});

afterAll(() => {
  if (server.shutdown) {
    server.shutdown();
  }
});
