import { useQuery } from '@tanstack/react-query';
import { api } from '../utils/api';

export const useDocuments = () => {
  return useQuery({
    queryKey: ['documents'],
    queryFn: api.getDocuments,
    refetchOnWindowFocus: false,
  });
};
