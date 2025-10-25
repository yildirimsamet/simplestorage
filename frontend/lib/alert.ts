import Swal from 'sweetalert2';

export const showAlert = {
  success: (message: string = 'Operation completed successfully') => {
    return Swal.fire({
      icon: 'success',
      title: 'Success!',
      text: message,
      confirmButtonColor: '#2563eb',
    });
  },

  error: (message: string = 'An error occurred') => {
    return Swal.fire({
      icon: 'error',
      title: 'Error!',
      text: message,
      confirmButtonColor: '#dc2626',
    });
  },

  confirm: (message: string = 'Are you sure?') => {
    return Swal.fire({
      icon: 'warning',
      title: 'Confirmation',
      text: message,
      showCancelButton: true,
      confirmButtonColor: '#2563eb',
      cancelButtonColor: '#6b7280',
      confirmButtonText: 'Yes',
      cancelButtonText: 'Cancel',
    });
  },
};
