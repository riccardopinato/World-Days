import 'dart:math';

import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../domain/observance.dart';
import '../../l10n/app_localizations.dart';

class DailyQuizPage extends StatefulWidget {
  const DailyQuizPage({super.key, required this.controller});

  final AppController controller;

  @override
  State<DailyQuizPage> createState() => _DailyQuizPageState();
}

class _DailyQuizPageState extends State<DailyQuizPage> {
  late Observance question;
  late List<String> options;
  String? selected;

  @override
  void initState() {
    super.initState();
    _buildQuestion(DateTime.now());
  }

  void _buildQuestion(DateTime now, {int salt = 0}) {
    final records = widget.controller.search('');
    if (records.isEmpty) {
      throw StateError('quiz_catalog_empty');
    }

    final seed = now.year * 10000 + now.month * 100 + now.day + salt;
    final random = Random(seed);
    question = records[random.nextInt(records.length)];

    final authorities = records
        .map((record) => record.authority.name)
        .where((value) => value != question.authority.name)
        .toSet()
        .toList(growable: false);

    final distractors = <String>[];
    final pool = [...authorities];
    while (pool.isNotEmpty && distractors.length < 3) {
      distractors.add(pool.removeAt(random.nextInt(pool.length)));
    }

    options = [question.authority.name, ...distractors];
    options.shuffle(random);
    selected = null;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final correct = selected == question.authority.name;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.dailyQuiz)),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(22),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.quizAuthorityQuestion,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 14),
                  Text(
                    question.title,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 18),
          for (final option in options) ...[
            FilledButton.tonal(
              onPressed: selected == null
                  ? () => setState(() => selected = option)
                  : null,
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(option),
              ),
            ),
            const SizedBox(height: 10),
          ],
          if (selected != null) ...[
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      correct
                          ? Icons.check_circle_rounded
                          : Icons.info_outline_rounded,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        correct
                            ? l10n.correctAnswer
                            : '${l10n.wrongAnswer}. ${question.authority.name}',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: () => setState(
                () => _buildQuestion(
                  DateTime.now(),
                  salt: DateTime.now().millisecond + options.length,
                ),
              ),
              icon: const Icon(Icons.refresh_rounded),
              label: Text(l10n.quizTryAnother),
            ),
          ],
        ],
      ),
    );
  }
}
