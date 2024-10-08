import 'package:client/core/utils.dart';
import 'package:client/core/widgets/loader.dart';
import 'package:client/features/auth/view/pages/signup_page.dart';
import 'package:client/features/auth/view/widgets/auth_gradient_button.dart';
import 'package:client/features/auth/view/widgets/custom_field.dart';
import 'package:client/features/auth/viewmodel/auth_viewmodel.dart';
import 'package:client/features/repositories/auth_remote_repository.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fpdart/fpdart.dart';

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
  final emailControler = TextEditingController();
  final passwordControler = TextEditingController();
  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    // TODO: implement dispose
    emailControler.dispose();
    passwordControler.dispose();
    super.dispose();
    formKey.currentState?.validate();
  }

  @override
  Widget build(BuildContext context) {
    final isLoading = ref.watch(authViewmodelProvider)?.isLoading == true;

    ref.listen(
      authViewmodelProvider,
      (_, next) {
        next?.when(
          data: (data) {
            // TODO: Navigate to the home page
            // Navigator.push(context, MaterialPageRoute(builder: (context) {
            //   return const HomePage();
            // }));
          },
          error: (error, st) {
            showSnackBar(context, error.toString(), Colors.red);
          },
          loading: () {},
        );
      },
    );

    return Scaffold(
      appBar: AppBar(),
      body: isLoading
          ? const Loader()
          : Padding(
              padding: const EdgeInsets.all(15.0),
              child: Form(
                key: formKey,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text(
                      'Sign In',
                      style: TextStyle(
                        fontSize: 50,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 30),
                    CustomField(
                      hintText: 'Email',
                      controller: emailControler,
                    ),
                    const SizedBox(height: 15),
                    CustomField(
                      hintText: 'Password',
                      controller: passwordControler,
                      isObscureText: true,
                    ),
                    const SizedBox(height: 20),
                    AuthGradientButton(
                      buttonText: 'Sign in',
                      onTap: () async {
                        if (formKey.currentState!.validate()) {
                          await ref
                              .read(authViewmodelProvider.notifier)
                              .loginUser(
                                email: emailControler.text,
                                password: passwordControler.text,
                              );
                        } else {
                          showSnackBar(context, 'Invalid form', Colors.red);
                        }
                      },
                    ),
                    const SizedBox(height: 20),
                    GestureDetector(
                      onTap: () {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => const SignupPage()));
                      },
                      child: RichText(
                          text: TextSpan(
                              text: "Don't have an account? ",
                              style: Theme.of(context).textTheme.titleMedium,
                              children: const [
                            TextSpan(
                              text: 'Sign Up',
                              style: TextStyle(
                                color: Colors.blue,
                                fontWeight: FontWeight.bold,
                              ),
                            )
                          ])),
                    )
                  ],
                ),
              ),
            ),
    );
  }
}
