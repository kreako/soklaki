export const userInitials = (user) => {
  if (user.firstname == null || user.lastname == null) {
    return null;
  }
  const f = user.firstname[0].toUpperCase();
  const l = user.lastname[0].toUpperCase();
  return `${f}${l}`;
};
