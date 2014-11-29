# coding: utf-8
from guardian.core import ObjectPermissionChecker
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized


class GuardianAuthorization(DjangoAuthorization):
    def base_checks(self, request, model_klass):
        class_ = super(GuardianAuthorization, self).base_checks(
            request, model_klass)

        if not class_:
            raise Unauthorized('You are not allowed to access this resource.')

        # User must be authenticated
        if not request.user.is_authenticated():
            return Unauthorized('You are not allowed to access this resource.')

        return class_

    def has_permission(self, object_list, bundle, permission_type):
        model = getattr(object_list, 'model', bundle.obj._meta.model)

        class_ = self.base_checks(bundle.request, model)
        permission = '{}_{}'.format(permission_type, class_._meta.model_name)

        objects = []
        checker = ObjectPermissionChecker(bundle.request.user)
        for obj in object_list:
            if checker.has_perm(permission, obj):
                objects.append(obj)

        return objects

    def read_list(self, object_list, bundle):
        return self.has_permission(object_list, bundle, 'view')

    def create_list(self, object_list, bundle):
        return self.has_permission(object_list, bundle, 'add')

    def update_list(self, object_list, bundle):
        return self.has_permission(object_list, bundle, 'change')

    def delete_list(self, object_list, bundle):
        return self.has_permission(object_list, bundle, 'delete')

    def read_detail(self, object_list, bundle):
        return bool(self.has_permission([bundle.obj], bundle, 'view'))

    def create_detail(self, object_list, bundle):
        return bool(self.has_permission([bundle.obj], bundle, 'add'))

    def update_detail(self, object_list, bundle):
        return bool(self.has_permission([bundle.obj], bundle, 'change'))

    def delete_detail(self, object_list, bundle):
        return bool(self.has_permission([bundle.obj], bundle, 'delete'))
